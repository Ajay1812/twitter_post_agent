import tweepy
from dotenv import load_dotenv
from langchain.tools import tool
import os
import re
load_dotenv()

@tool
def twitter_post(final_post: str) -> str:
    """This tool will post the daily update on twiiter"""
    try:
        client = tweepy.Client(
            consumer_key=os.environ["TWITTER_CONSUMER_API_KEY"],
            consumer_secret=os.environ["TWITTER_CONSUMER_API_SECRET"],
            access_token=os.environ["ACCESS_TOKEN"],
            access_token_secret=os.environ["SECRET_TOKEN"]
        )
        # print("Final_Post: ", final_post, type(final_post))
        client.create_tweet(text=final_post)
        return "post created."
    except Exception as e:
        return f"Tweet failed: {e}"
    
# final_post = """
# Day 2: Today I learned how LangGraph uses persistence for fault tolerance. I also studied ACID properties in SQL and BASE principles in NoSQL databases.
# """
# print(twitter_post(final_post))

def clean_tweet_text(text: str) -> str:
    """
    Cleans the tweet content by:
    - Removing emojis and special symbols
    - Replacing emoji bullets with hyphens
    - Stripping extra whitespace
    - Ensuring tweet length under 280 characters
    """
    text = text.replace("🔹", "-").replace("•", "-").replace("→", "-")
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > 280:
        text = text[:277].rsplit(" ", 1)[0] + "..."
    return text
