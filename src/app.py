from flask import Flask, request, redirect, jsonify
from link_shortner import LinkShortner
from db import connect_redis
import random


#initialize flask app
app = Flask(__name__)

#initialize redis cache
redis_client = connect_redis()

#initialize Link Shortner service
lk = LinkShortner(redis_client)


# def generate_key():
#     return ''.join(random.choices(charset, k=key_length))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json['url']
    short_link = lk.short_link(long_url)
    return jsonify({'short_url': f'{short_link}'})

@app.route('/<key>')
def redirect_url(key):
    long_url = redis_client.get(key)
    if long_url:
        return redirect(long_url.decode("utf-8"))
    return 'URL not found', 404

if __name__ == "__main__":
    app.run(debug=True)
