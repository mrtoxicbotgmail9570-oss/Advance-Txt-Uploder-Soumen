#🇳‌🇮‌🇰‌🇭‌🇮‌🇱‌
# Add your details here and then deploy by clicking on HEROKU Deploy button
import os
from os import environ

API_ID = int(environ.get("API_ID", "38498066"))
API_HASH = environ.get("API_HASH", "c9696114751feacdeb1b4487f5839a1a")
BOT_TOKEN = environ.get("BOT_TOKEN", "")

OWNER = int(environ.get("OWNER", "8446475678"))
CREDIT = environ.get("CREDIT", "💥 @CinderellaContactBot")
cookies_file_path = os.getenv("cookies_file_path", "youtube_cookies.txt")

TOTAL_USER = os.environ.get('TOTAL_USERS', '8723278238,8480660521,7988815969,6660248311,8680968748,8745263057,8703802029').split(',')
TOTAL_USERS = [int(user_id) for user_id in TOTAL_USER]

AUTH_USER = os.environ.get('AUTH_USERS', '8723278238,8480660521,7988815969,6660248311,8680968748,8745263057,8703802029').split(',')
AUTH_USERS = [int(user_id) for user_id in AUTH_USER]
if int(OWNER) not in AUTH_USERS:
    AUTH_USERS.append(int(OWNER))

