from utils.states import TweetState, TweetEvaluation
from config.model import gemini_model
from langchain_core.messages import SystemMessage, HumanMessage

structured_llm = gemini_model().with_structured_output(TweetEvaluation)

def generate_tweet(state: TweetState) -> TweetState:
    messages = [SystemMessage(content="""
You are a helpful assistant who analyzes the user's Obsidian notes from today and generates a clear daily update for social media.

Your tasks are:

1. Analyze the Obsidian notes provided.
2. Identify the main topic or concept the user learned today.
3. Write a short summary (1–2 sentences) of what was learned.
4. Generate a concise tweet under 280 characters, describing what the user learned today in a clear and professional tone.
5. Include appropriate hashtags (e.g., #100DaysOfCode, #Learning, #Tech, etc.), keeping the tweet relevant but simple.

Avoid sarcasm, humor, exaggeration, or casual slang. Do not ask questions or include emojis. Your tone should be informative, focused, and authentic.
"""),    
    HumanMessage(content=f"""
    Here are my Obsidian notes from today:

    {state['notes']}

    Please:
    1. Identify the main topic or concept I learned today.
    2. Write a short summary (1–2 sentences) of what I learned.
    3. Generate a tweet under 280 characters, clearly stating what I learned today in a professional and concise tone. Add 1–2 relevant hashtags (e.g., #100DaysOfCode, #Learning, #Tech).

    No jokes, sarcasm, or casual language — keep it focused and authentic.

    This is version {state['iteration'] + 1}.
    """)
    ]
    print("Generating tweet...")
    response = gemini_model().invoke(messages).content
    return {"tweet": response, "tweet_history": [response]}

def evaluate_tweet(state: TweetState) -> TweetState:
    """Evaluate learning tweet generated from Obsidian notes"""
    messages = [
        SystemMessage(content="""
You are a precise and thoughtful evaluator for learning update tweets. Your job is to review the tweet based on the user's notes and assess how well it communicates what they learned.

You care about clarity, relevance, and completeness — not humor or virality.

Use the following criteria to evaluate:

1. **Accuracy** – Does the tweet reflect the content and essence of the provided notes?
2. **Clarity** – Is the tweet clearly written and easy to understand for others?
3. **Brevity** – Is the tweet concise and under 280 characters?
4. **Professional Tone** – Does the tweet maintain a neutral, focused, and respectful tone suitable for a learning update?
5. **Relevance** – Does it convey the value or takeaway of the learning?

Auto-reject if:
- It’s vague, generic, or doesn’t reflect the actual notes.
- It exceeds 280 characters.
- It sounds promotional, sarcastic, or unrelated to the learning.
- It uses unclear jargon without explanation.

Respond ONLY in the following structured format:
- evaluation: "approved" or "needs_improvement"
- feedback: A short paragraph explaining strengths and weaknesses.
        """),
        HumanMessage(content=f"""
Evaluate the following tweet based on these Obsidian notes:

Notes:
{state['notes']}

Tweet:
"{state['tweet']}"
        """)
    ]
    print("Evaluating tweet...")
    response = structured_llm.invoke(messages)
    return {
        "evaluation": response.evaluation,
        "feedback": response.feedback,
        "feedback_history": state.get("feedback_history", []) + [response.feedback],
    }

def optimize_tweet(state: TweetState) -> TweetState:
    """Improve the learning tweet for clarity, tone, and tweet formatting"""
    messages = [
        SystemMessage(content="""
You are a writing assistant that improves learning-related tweets. Your job is to take the original tweet and feedback, and rewrite it to better reflect what the user learned.

Your tone should be:
- Professional
- Clear and concise
- Focused on the topic of learning

Your constraints:
- Must reflect the topic and notes accurately
- Stay under 280 characters
- Avoid slang, jokes, or sarcasm
- Include 1–2 relevant hashtags if not already present (e.g., #100DaysOfCode, #Learning, #Tech)

Only return the improved tweet — no explanation.
        """),
        HumanMessage(content=f"""
Improve the tweet based on this feedback:
"{state['feedback']}"

Notes: "{state['notes']}"
Original Tweet:
"{state['tweet']}"
        """)
    ]
    print("Optimizing tweet...")
    response = gemini_model().invoke(messages).content
    iteration = state["iteration"] + 1
    return {
        "tweet": response,
        "iteration": iteration,
        "tweet_history": state.get("tweet_history", []) + [response],
    }

def route_evaluation(state: TweetState):
    if state['evaluation'] == "approved" or state['iteration'] >= state["max_iteration"]:
        return "approved"
    else:
        return "needs_improvements"