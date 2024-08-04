from flask import Blueprint

from flask import request, redirect, jsonify
from linkshortener.link_shortner import LinkShortner
from ip.ip_config import ip_info_init, get_geo_data
from db.db import connect_redis




#initialize flask app
api = Blueprint("api", __name__)

#initialize redis cache
redis_client = connect_redis()

ip_handler = ip_info_init()

#initialize Link Shortner service
lk = LinkShortner(redis_client)



@api.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json['url']
    short_link = lk.short_link(long_url)
    return jsonify({'short_url': f'{short_link}'})

@api.route('/<key>', methods=["GET"])
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

