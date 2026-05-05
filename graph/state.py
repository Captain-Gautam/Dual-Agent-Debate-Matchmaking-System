"""
State definition for the debate workflow using LangGraph.
"""

from typing import TypedDict, List


class Message(TypedDict):
    """Individual message in the debate."""
    agent: str  # "agent_1", "agent_2", or "moderator"
    content: str
    round: int


class DebateState(TypedDict):
    """
    State schema for the debate workflow.
    
    Attributes:
        topic: The debate topic
        messages: List of all messages in the debate
        current_round: Current round number
        max_rounds: Maximum number of rounds
        history: Formatted history string for context
        summary: Final summary from moderator
        is_complete: Whether the debate is finished
    """
    topic: str
    messages: List[Message]
    current_round: int
    max_rounds: int
    history: str
    summary: str
    is_complete: bool
