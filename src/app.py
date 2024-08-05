from flask import Flask, request, redirect, render_template, url_for
from dotenv import load_dotenv
from src.db.db import connect_redis
from src.ip.ip_config import ip_info_init, get_geo_data
from src.api.routes import api

import datetime
import random
import string
import os

load_dotenv()

key_length = int(os.getenv("KEY_LEN"))
base_link = os.getenv("BASE_LINK")
charset = string.ascii_letters + string.digits

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')


redis_client = connect_redis()

ip_handler = ip_info_init()


def generate_key():
    return ''.join(random.choices(charset, k=key_length))

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/shorten', methods=["GET",'POST'])
def shorten_url():
    long_url = request.form['url']
    while True:
        key = generate_key()
        if not redis_client.exists(key):
            redis_client.set(key, long_url)
            return render_template("index.html", short_url= f'{base_link}/{key}')

@app.route('/<key>')
def redirect_url(key):
    long_url = redis_client.get(key)

    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get("User-Agent")
    device = "mobile" if "Mobi" in user_agent else "desktop"
    timestamp = datetime.datetime.now()
    geo_location = get_geo_data(ip_handler, ip_address)

    print(ip_address, user_agent, device, timestamp, geo_location)
    if long_url:
        return redirect(long_url.decode("utf-8"))
    return 'URL not found', 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
