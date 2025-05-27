from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
