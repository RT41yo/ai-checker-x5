import os
from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "25"))

DATA_CASES_PATH = os.getenv("DATA_CASES_PATH", "data/demo_cases.json")
DATA_RUBRIC_PATH = os.getenv("DATA_RUBRIC_PATH", "data/demo_rubric.json")
