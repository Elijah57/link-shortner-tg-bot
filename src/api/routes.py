from flask import Flask, request, redirect, jsonify, Blueprint
from dotenv import load_dotenv
from db.db import connect_redis
from ip.ip_config import ip_info_init, get_geo_data
import datetime
import random
import string
import os

load_dotenv()

key_length = int(os.getenv("KEY_LEN"))
base_link = os.getenv("BASE_LINK")
charset = string.ascii_letters + string.digits

api = Blueprint("api", __name__)


redis_client = connect_redis()

ip_handler = ip_info_init()


def generate_key():
    return ''.join(random.choices(charset, k=key_length))


@api.route('/shorten', methods=["GET",'POST'])
def shorten_url():
    long_url = request.json['url']
    while True:
        key = generate_key()
        if not redis_client.exists(key):
            redis_client.set(key, long_url)
            return jsonify({"short_url":f'{base_link}/{key}'}) 

@api.route('/<key>')
def redirect_url(key):
    long_url = redis_client.get(key)

    ip_address = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    device = "mobile" if "Mobi" in user_agent else "desktop"
    timestamp = datetime.datetime.now()
    geo_location = get_geo_data(ip_handler, ip_address)

    print(ip_address, user_agent, device, timestamp, geo_location)
    if long_url:
        return redirect(long_url.decode("utf-8"))
    return 'URL not found', 404



