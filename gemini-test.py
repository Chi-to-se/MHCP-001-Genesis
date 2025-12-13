import google.generativeai as genai
import os

#Load env
from dotenv import load_dotenv
load_dotenv()

MY_API_KEY = os.getenv('API_KEY')
