import os
from dotenv import load_dotenv

load_dotenv()

TokenBot = os.environ.get("token_bot")
ApiId = os.environ.get("api_id")
ApiHash = os.environ.get("api_hash")
