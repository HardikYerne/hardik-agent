import os
from dotenv import load_dotenv

load_dotenv()

ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Hardik")
LANGUAGE = os.getenv("LANGUAGE", "en")
VERSION = os.getenv("VERSION", "1.0.0")