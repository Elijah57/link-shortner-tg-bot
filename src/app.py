from flask import Flask, request, redirect, jsonify
from dotenv import load_dotenv
from db import connect_redis
import random
import string
import os

load_dotenv()

key_length = int(os.getenv("KEY_LEN"))
base_link = os.getenv("BASE_LINK")
charset = string.ascii_letters + string.digits

app = Flask(__name__)

redis_client = connect_redis()



def generate_key():
    return ''.join(random.choices(charset, k=key_length))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json['url']
    while True:
        key = generate_key()
        if not redis_client.exists(key):
            redis_client.set(key, long_url)
            return jsonify({'short_url': f'{base_link}/{key}'})

@app.route('/<key>')
def redirect_url(key):
    long_url = redis_client.get(key)
    if long_url:
        return redirect(long_url.decode("utf-8"))
    return 'URL not found', 404

if __name__ == "__main__":
    app.run(debug=True)
