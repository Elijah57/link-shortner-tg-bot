import redis
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("HOST")
port = os.getenv("PORT")
access_key = os.getenv("ACCESS_KEY")

def connect_redis():

    try:
        redis_client = redis.StrictRedis(
            host= host,
            port= 6379,
            password= access_key,
            ssl= True
        )
        redis_client.ping()
        print("Connected to Redis successfully!")
        return redis_client


    except redis.ConnectionError as e:
        print(f"Could not connect to Redis: {e}")
        return None

   
