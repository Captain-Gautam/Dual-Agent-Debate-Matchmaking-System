"""
LangGraph workflow for managing the debate between two agents.
"""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from .state import DebateState, Message
from agents.debate_agents import (
    create_agent_1, 
    create_agent_2, 
    create_moderator,
    get_agent_1_response,
    get_agent_2_response,
    get_moderator_summary
)


def format_history(messages: list) -> str:
    """Format debate history for context."""
    if not messages:
        return "No arguments yet."
    
    formatted = []
    for msg in messages:
        agent_name = {
            "agent_1": "Agent Alpha",
            "agent_2": "Agent Beta",
            "moderator": "Moderator"
        }.get(msg["agent"], msg["agent"])
        
        formatted.append(f"**{agent_name} (Round {msg['round']}):**\n{msg['content']}\n")
    
    return "\n".join(formatted)


def agent_1_node(state: DebateState) -> Dict[str, Any]:
    """Node for Agent 1 to provide argument."""
    # Get agent and generate response
    agent = create_agent_1(state.get("api_key", ""))
    history = format_history(state["messages"])
    
    response = get_agent_1_response(agent, state["topic"], history)
    
    # Create message
    message: Message = {
        "agent": "agent_1",
        "content": response,
        "round": state["current_round"]
    }
    
    # Update state
    messages = state["messages"] + [message]
    
    return {
        "messages": messages,
        "history": format_history(messages)
    }


def agent_2_node(state: DebateState) -> Dict[str, Any]:
    """Node for Agent 2 to provide counter-argument."""
    # Get agent and generate response
    agent = create_agent_2(state.get("api_key", ""))
    history = format_history(state["messages"])
    
    response = get_agent_2_response(agent, state["topic"], history)
    
    # Create message
    message: Message = {
        "agent": "agent_2",
        "content": response,
        "round": state["current_round"]
    }
    
    # Update state
    messages = state["messages"] + [message]
    
    return {
        "messages": messages,
        "history": format_history(messages),
        "current_round": state["current_round"] + 1
    }


def moderator_node(state: DebateState) -> Dict[str, Any]:
    """Node for moderator to summarize the debate."""
    moderator = create_moderator(state.get("api_key", ""))
    history = format_history(state["messages"])
    
    summary = get_moderator_summary(moderator, state["topic"], history)
    
    return {
        "summary": summary,
        "is_complete": True
    }


def should_continue(state: DebateState) -> str:
    """Determine if debate should continue or end."""
    if state["current_round"] > state["max_rounds"]:
        return "summarize"
    return "continue"


def create_debate_workflow(api_key: str) -> StateGraph:
    """
    Create the LangGraph workflow for the debate.
    
    Args:
        api_key: Google API key for Gemini
        
    Returns:
        Compiled StateGraph workflow
    """
    # Create the graph
    workflow = StateGraph(DebateState)
    
    # Add nodes
    workflow.add_node("agent_1", agent_1_node)
    workflow.add_node("agent_2", agent_2_node)
    workflow.add_node("moderator", moderator_node)
    
    # Add edges
    workflow.set_entry_point("agent_1")
    workflow.add_edge("agent_1", "agent_2")
    
    # Conditional edge from agent_2
    workflow.add_conditional_edges(
        "agent_2",
        should_continue,
        {
            "continue": "agent_1",
            "summarize": "moderator"
        }
    )
    
    workflow.add_edge("moderator", END)
    
    # Compile the graph
    return workflow.compile()


def run_debate(topic: str, max_rounds: int, api_key: str):
    """
    Run a complete debate and yield state updates.
    
    Args:
        topic: The debate topic
        max_rounds: Number of rounds for the debate
        api_key: Google API key
        
    Yields:
        Updated state after each step
    """
    # Create workflow
    app = create_debate_workflow(api_key)
    
    # Initialize state
    initial_state = {
        "topic": topic,
        "messages": [],
        "current_round": 1,
        "max_rounds": max_rounds,
        "history": "",
        "summary": "",
        "is_complete": False,
        "api_key": api_key
    }
    
    # Run the workflow and stream results
    for state in app.stream(initial_state):
        yield state
