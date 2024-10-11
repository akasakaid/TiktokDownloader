import os
import databases
from dotenv import load_dotenv

load_dotenv()

token_bot = os.environ.get("token_bot")
api_id = os.environ.get("api_id")
api_hash = os.environ.get("api_hash")
database_name = "tiktok-downloader"
database_url = os.getenv("database_url")
database_port = os.getenv("database_port")
database_user = os.getenv("database_user")
database_pass = os.getenv("database_pass")

DATABASE = f"mysql+aiomysql://{database_user}:{database_pass}@{database_url}:{database_port}/{database_name}"
