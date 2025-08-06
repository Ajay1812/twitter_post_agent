from utils.loader import load_markdown_documents  
from utils.graph import workflow  
from tools.twitter import clean_tweet_text, twitter_post 
from config.model import gemini_model
from langchain_core.messages import HumanMessage
from datetime import datetime
from dotenv import load_dotenv
import json
load_dotenv()

def run_tweet_workflow(markdown_path: str):
    documents = load_markdown_documents(markdown_path)
    
    if not documents:
        print("No notes found.")
        return
    combined_notes = "\n".join(doc.page_content for doc in documents)

    today = datetime.now().strftime("%Y-%m-%d")
    initial_state = {
        "notes": combined_notes,
        "tweet": "",
        "evaluation": "",
        "feedback": "",
        "feedback_history": [],
        "iteration": 1,
        "max_iteration": 5,
        "tweet_history": [],
        "date": today
    }

    final_state = workflow.invoke(initial_state)
    print("✅ Final Tweet:")
    print(final_state["tweet"])

    return final_state

if __name__ == "__main__":
    final_tweet_state = run_tweet_workflow("/home/nf/Documents/Projects/twitter_post_agent/data/")
    tweet = final_tweet_state["tweet"]
    llm = gemini_model().bind_tools([twitter_post])
    print("🤖 Model invoking tool…")
    
    response = llm.invoke([HumanMessage(content=f"Post the following tweet:\n{tweet}")])
    # print("RESPONSE: ", response)
    
    func = response.additional_kwargs.get("function_call")
    if func:
        final_post = json.loads(func["arguments"])
        # print("final_post: ", final_post, type(final_post))
        post = clean_tweet_text(final_post["final_post"])
        result = twitter_post.invoke({"final_post": post})
        print("🧾 Twitter Reply:", result)
    else:
        print("⚠️ No tool call found.")