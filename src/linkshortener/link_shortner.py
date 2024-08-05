# testing phase

import random
import string

# print("Welcome to my link shortner")
# long_link = input("Input the link: ")

# print(f"this is the link you provided: {long_link}")


class LinkShortner:

    def __init__(self) -> None:
        self.db = {}
        self.key_length = 6
        self.charset = string.ascii_letters + string.digits
        self.base_link = "https://sht.ly/"

    def generate_key(self):
        return "".join(random.choices(self.charset, k=self.key_length))
    
    def shorten_url(self, long_url:str):
        while True:
            key = self.generate_key()
            if key not in self.db:
                self.db[key] = long_url
                return key
            
    def short_link(self, long_url:str):
        return self.base_link + self.shorten_url(long_url)
    
    def get_long_url(self, key):
        if key in self.db:
            return self.db[key]
        return "Not Found"
            
# linker = LinkShortner()
# short = linker.short_link(long_link)
# print(short)

# skey = short[-6:]
# print(skey)
# print(linker.get_long_url(skey))

        