from utils.states import TweetState, TweetEvaluation
from config.model import gemini_model
from langchain_core.messages import SystemMessage, HumanMessage

structured_llm = gemini_model().with_structured_output(TweetEvaluation)

def generate_tweet(state: TweetState) -> TweetState:
    messages = [SystemMessage(content="""
You are a tweet composer for a developer who shares daily learning updates.

Your task:
- Begin with: "Day {n}: Today I learned about"
- Summarize each key topic as a bullet point using "-"
- Each bullet point should be one concise line
- Use a formal and informative tone
- Do not use emojis, hashtags, or casual phrases
- The entire output must stay under 280 characters
- Output only the tweet. Do not include explanations or multiple versions.

Make sure the tweet is easy to read and valuable for others following the developer’s learning journey.
"""),    
    HumanMessage(content=f"""
These are my Obsidian notes for today:

{state['notes']}

Please:
1. Summarize the key points I learned.
2. Create a tweet starting with "Day {state['iteration'] + 1}: Today I learned about"
3. Use bullet points and one-line summaries, all within 280 characters.
4. No emojis or hashtags. Keep it professional and concise.
""")

    ]
    print("Generating tweet...")
    response = gemini_model().invoke(messages).content
    return {"tweet": response, "tweet_history": [response]}

def evaluate_tweet(state: TweetState) -> TweetState:
    """Evaluate learning tweet generated from Obsidian notes"""
    messages = [SystemMessage(content="""
You are a tweet evaluator. You must assess whether the tweet meets professional learning standards.

Rules:
- Evaluate the tweet based *only* on the notes provided.
- Use these criteria:
  1. Accuracy – Must match what the user learned.
  2. Clarity – Easy to understand.
  3. Brevity – Under 280 characters.
  4. Professional Tone – No slang, hype, or informal tone.
  5. Relevance – Must convey a clear, focused learning outcome.

Auto-reject if:
- The tweet is vague or too generic
- It does not directly reflect the notes
- It sounds promotional, sarcastic, or casual
- It exceeds 280 characters

Output format (strict):
- evaluation: "approved" or "needs_improvement"
- feedback: A specific, concise explanation (~1–2 sentences)

Do not include any extra content.
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
    messages = [SystemMessage(content="""
You are a strict tweet rewriting assistant.

Rules:
- Use the user’s notes and prior feedback to revise the tweet.
- Make the tweet professional, clear, and brief.
- Avoid all of the following: casual language, slang, jokes, emojis, or promotional tones.
- Stay strictly under 280 characters.
- Add 1–2 relevant hashtags only if they fit the topic (e.g., #100DaysOfCode, #Tech, #AI).

Do not add extra opinions or unrelated commentary.
Do not output multiple versions — return only the single best tweet.

Final output: Just the improved tweet. Nothing else.
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