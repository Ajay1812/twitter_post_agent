import tweepy
from dotenv import load_dotenv
from langchain.tools import tool
import os
load_dotenv()

@tool
def twitter_post(final_post: str):
    """This tool will post the daily update on twiiter"""
    try:
        client = tweepy.Client(
            consumer_key=os.environ["TWITTER_CONSUMER_API_KEY"],
            consumer_secret=os.environ["TWITTER_CONSUMER_API_SECRET"],
            access_token=os.environ["ACCESS_TOKEN"],
            access_token_secret=os.environ["SECRET_TOKEN"]
        )

        client.create_tweet(text=final_post)
        return "Tweet posted successfully."
    except Exception as e:
        return f"Tweet failed: {e}"