from flask import Flask, request, redirect, jsonify, render_template
from link_shortner import LinkShortner
from ip_config import ip_info_init, get_geo_data
from db import connect_redis
import random


#initialize flask app
app = Flask(__name__)

#initialize redis cache
redis_client = connect_redis()

ip_handler = ip_info_init()

#initialize Link Shortner service
lk = LinkShortner(redis_client)

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    if request.method == 'POST':
        long_url = request.form['url']
        short_url = lk.short_link(long_url)
    return render_template('index.html', short_url=short_url)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['url']
    short_link = lk.short_link(long_url)
    return render_template('index.html', short_url=short_link)
    # return jsonify({'short_url': f'{short_link}'})

@app.route('/<key>', methods=["GET"])
def redirect_url(key):
    long_url = lk.get_long_url(key)

    ip_address = request.headers['X-Forwarded-For'].split(',')[0] if request.headers.get('X-Forwarded-For') else request.remote_addr
    user_agent = request.headers.get("User-Agent")
    device = "mobile" if "Mobi" in user_agent else "desktop"
    geo_data = get_geo_data(ip_handler, ip_address)

    print(ip_address, user_agent, device, geo_data)
    if long_url:
        return redirect(long_url.decode("utf-8"))
    return 'URL not found', 404

if __name__ == "__main__":
    app.run(debug=True)
