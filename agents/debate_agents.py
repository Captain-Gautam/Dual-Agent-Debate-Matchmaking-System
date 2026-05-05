"""
Agent creation and configuration for the debate system.
"""

import google.generativeai as genai
import time
from .prompts import AGENT_1_PROMPT, AGENT_2_PROMPT, MODERATOR_PROMPT


def create_agent_1(api_key: str, temperature: float = 0.7):
    """Create Agent Alpha - the logical and analytical debater."""
    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": temperature,
        "max_output_tokens": 300,
    }
    return genai.GenerativeModel('models/gemini-2.0-flash', generation_config=generation_config)


def create_agent_2(api_key: str, temperature: float = 0.8):
    """Create Agent Beta - the passionate and persuasive debater."""
    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": temperature,
        "max_output_tokens": 300,
    }
    return genai.GenerativeModel('models/gemini-2.0-flash', generation_config=generation_config)


def create_moderator(api_key: str, temperature: float = 0.5):
    """Create Moderator - the impartial judge and summarizer."""
    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": temperature,
        "max_output_tokens": 450,
    }
    return genai.GenerativeModel('models/gemini-2.0-flash', generation_config=generation_config)


def parse_topic_position(topic: str, agent_number: int) -> str:
    """Parse topic to assign positions when it contains 'vs' or 'versus'."""
    topic_lower = topic.lower()
    
    if ' vs ' in topic_lower or ' vs. ' in topic_lower:
        separator = ' vs ' if ' vs ' in topic_lower else ' vs. '
    elif ' versus ' in topic_lower:
        separator = ' versus '
    else:
        return ""
    
    parts = topic.split(separator, maxsplit=1) if separator == ' vs ' else topic.split(' vs. ' if ' vs. ' in topic_lower else ' versus ', maxsplit=1)
    
    if len(parts) == 2:
        side1 = parts[0].strip()
        side2 = parts[1].strip()
        
        if agent_number == 1:
            return f"\n**YOUR POSITION: You are arguing in favor of '{side1}'. Focus all your arguments on supporting '{side1}' and why it is superior to '{side2}'.**\n"
        else:
            return f"\n**YOUR POSITION: You are arguing in favor of '{side2}'. Focus all your arguments on supporting '{side2}' and why it is superior to '{side1}'.**\n"
    
    return ""


def get_agent_position(topic: str, agent_number: int) -> str:
    """Get the position/side that an agent is arguing for in a vs debate."""
    topic_lower = topic.lower()
    
    if ' vs ' in topic_lower or ' vs. ' in topic_lower:
        separator = ' vs ' if ' vs ' in topic_lower else ' vs. '
    elif ' versus ' in topic_lower:
        separator = ' versus '
    else:
        return ""
    
    parts = topic.split(separator, maxsplit=1) if separator == ' vs ' else topic.split(' vs. ' if ' vs. ' in topic_lower else ' versus ', maxsplit=1)
    
    if len(parts) == 2:
        side1 = parts[0].strip()
        side2 = parts[1].strip()
        return side1 if agent_number == 1 else side2
    
    return ""


def get_agent_1_response(agent, topic: str, history: str) -> str:
    """Get response from Agent 1."""
    position_instruction = parse_topic_position(topic, agent_number=1)
    prompt = AGENT_1_PROMPT.format(topic=topic, history=history, position_instruction=position_instruction)
    time.sleep(2)
    response = agent.generate_content(prompt)
    return response.text


def get_agent_2_response(agent, topic: str, history: str) -> str:
    """Get response from Agent 2."""
    position_instruction = parse_topic_position(topic, agent_number=2)
    prompt = AGENT_2_PROMPT.format(topic=topic, history=history, position_instruction=position_instruction)
    time.sleep(2)
    response = agent.generate_content(prompt)
    return response.text


def get_moderator_summary(moderator, topic: str, history: str) -> str:
    """Get debate summary from moderator."""
    prompt = MODERATOR_PROMPT.format(topic=topic, history=history)
    time.sleep(2)
    response = moderator.generate_content(prompt)
    return response.text
