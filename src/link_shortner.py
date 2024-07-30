import os
from dotenv import load_dotenv
import random
import string

load_dotenv()

key_length = int(os.getenv("KEY_LEN"))
base_link = os.getenv("BASE_LINK")


class LinkShortner:

    def __init__(self, redis_client) -> None:
        self.key_length = key_length
        self.charset = string.ascii_letters + string.digits
        self.redis_client = redis_client
        self.base_link = base_link

    def generate_key(self):
        return "".join(random.choices(self.charset, k=self.key_length))
    
    def shorten_url(self, long_url:str):
        while True:
            key = self.generate_key()
            if not self.redis_client.exists(key):
                self.redis_client.set(key, long_url)
                return key
            
    def short_link(self, long_url:str):
        return self.base_link + self.shorten_url(long_url)
    
    def get_long_url(self, key):
        long_url = self.redis_client.get(key)
        return long_url if long_url else "Not Found"
            


        
