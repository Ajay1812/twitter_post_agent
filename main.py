from utils.loader import load_markdown_documents  
from utils.graph import workflow  
from datetime import datetime

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
    run_tweet_workflow("/home/nf/Documents/Projects/twitter_post_agent/data/")
