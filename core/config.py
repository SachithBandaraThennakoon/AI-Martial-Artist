import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")


settings = Settings()