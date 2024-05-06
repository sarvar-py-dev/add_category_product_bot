import os

from dotenv import load_dotenv
from redis_dict import RedisDict

load_dotenv('.env')

TOKEN = os.getenv('BOT_TOKEN')
ADMIN_LIST: list[int] = []  # there is admins ids

database = RedisDict('products')
