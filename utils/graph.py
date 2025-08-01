from langgraph.graph import StateGraph, START, END
from utils.nodes import generate_tweet, evaluate_tweet, optimize_tweet, route_evaluation
from utils.states import TweetState

graph = StateGraph(TweetState)
graph.add_node("generate", generate_tweet)
graph.add_node("evaluate", evaluate_tweet)
graph.add_node("optimize", optimize_tweet)

graph.add_edge(START, "generate")
graph.add_edge("generate", "evaluate")

graph.add_conditional_edges("evaluate", route_evaluation, {"approved": END, "needs_improvements": "optimize"})
graph.add_edge("optimize", "evaluate")
workflow = graph.compile()