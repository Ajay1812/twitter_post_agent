from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

def gemini_model():
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite-preview-06-17",
        api_key=os.environ["GEMINI_API_KEY"]
    )
    return model

