import ipinfo
import os
from dotenv import load_dotenv



load_dotenv()

access_token = os.getenv("IP_TOKEN")

def ip_info_init():
    try:
        handler = ipinfo.getHandler(access_token)
        return handler


    except Exception as e:
    # Handle any other exceptions
        print(f'An error occurred: {e}') 

def get_geo_data(ip_handler, ip_address):
    details = ip_handler.getDetails(ip_address)
    data = {}
    for key, value in details.__dict__.items():
        data[key] = value
    return data