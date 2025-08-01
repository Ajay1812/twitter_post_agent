from typing import Annotated, TypedDict, Literal
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages

class TweetState(TypedDict):
    notes: Annotated[list[str], add_messages] = Field(description="list of .md documents")
    tweet: str
    evaluation: Literal["approved", "needs_improvements"]
    feedback: str
    iteration: int
    max_iteration: int
    
    tweet_history: Annotated[list[str], add_messages] 
    feedback_history: Annotated[list[str], add_messages] 

class TweetEvaluation(BaseModel):
    evaluation: Literal["approved", "needs_improvements"] = Field(description="Final Evaluation result")
    feedback: str = Field(..., description="Feedback for the tweet.")
    
