from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Config:
    FILE_NAME: str = os.getenv("FILE_NAME")
    FILE_PATH: str = os.getenv("FILE_PATH")