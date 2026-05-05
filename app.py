"""
Streamlit application for the AI Debate System.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from graph.workflow import run_debate
from agents.debate_agents import get_agent_position

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Debate Arena",
    page_icon="🎭",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .agent-1 {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2196F3;
        margin: 10px 0;
        color: #0d47a1;
    }
    .agent-2 {
        background-color: #fce4ec;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #E91E63;
        margin: 10px 0;
        color: #880e4f;
    }
    .moderator {
        background-color: #f3e5f5;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #9C27B0;
        margin: 10px 0;
        color: #4a148c;
    }
    .judgment {
        background-color: #fff3e0;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF9800;
        margin: 20px 0;
        color: #e65100;
    }
    .round-header {
        font-size: 18px;
        font-weight: bold;
        color: #555;
        margin-top: 20px;
    }
    .agent-name {
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 8px;
    }
    .position-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #4caf50;
    }
    .position-box p {
        margin: 5px 0;
        font-size: 15px;
    }
    .position-alpha {
        color: #0d47a1;
        font-weight: 600;
    }
    .position-beta {
        color: #880e4f;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🎭 AI Debate Arena")
st.markdown("### Watch two AI agents debate on any topic using Google Gemini")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key input
    api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        value=os.getenv("GOOGLE_API_KEY", ""),
        help="Enter your Google Gemini API key"
    )
    
    st.markdown("---")
    
    # Debate settings
    st.subheader("Debate Settings")
    max_rounds = st.slider(
        "Number of Rounds",
        min_value=1,
        max_value=5,
        value=3,
        help="How many back-and-forth exchanges?"
    )
    
    st.markdown("---")
    
    # Agent info
    st.subheader("🤖 Meet the Debaters")
    
    with st.expander("Agent Alpha 🔵"):
        st.markdown("""
        **Style:** Logical & Analytical
        - Evidence-based arguments
        - Structured reasoning
        - Professional tone
        """)
    
    with st.expander("Agent Beta 🔴"):
        st.markdown("""
        **Style:** Passionate & Persuasive
        - Emotional appeals
        - Compelling narratives
        - Rhetorical questions
        """)
    
    st.markdown("---")
    
    if st.button("ℹ️ About"):
        st.info("""
        This app uses LangGraph to orchestrate a debate between two AI agents powered by Google Gemini.
        
        Each agent has a distinct personality and debate style, making for engaging discussions!
        """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Topic input
    topic = st.text_input(
        "🎯 Enter Debate Topic",
        placeholder="e.g., Is artificial intelligence a threat to humanity?",
        help="What should the agents debate about?"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    start_debate = st.button("🚀 Start Debate", type="primary", use_container_width=True)

# Debate area
if start_debate:
    if not api_key:
        st.error("❌ Please enter your Google Gemini API key in the sidebar!")
    elif not topic:
        st.error("❌ Please enter a debate topic!")
    else:
        st.markdown("---")
        st.markdown(f"### 📢 Debate Topic: *{topic}*")
        st.markdown("---")
        
        # Get agent positions if it's a "vs" debate (for display in agent headers)
        agent1_position = get_agent_position(topic, 1)
        agent2_position = get_agent_position(topic, 2)
        
        # Create containers for the debate
        debate_container = st.container()
        status_container = st.empty()
        
        current_round = 0
        
        try:
            # Run the debate
            with st.spinner("🎬 Debate in progress..."):
                for step_output in run_debate(topic, max_rounds, api_key):
                    # Extract state from the step output
                    # LangGraph returns dict with node names as keys
                    for node_name, state in step_output.items():
                        if state.get("messages"):
                            with debate_container:
                                # Get the latest message
                                latest_msg = state["messages"][-1]
                                
                                # Display round header if new round
                                if latest_msg["round"] != current_round:
                                    current_round = latest_msg["round"]
                                    st.markdown(f'<div class="round-header">🔔 Round {current_round}</div>', 
                                              unsafe_allow_html=True)
                                
                                # Display message based on agent
                                if latest_msg["agent"] == "agent_1":
                                    position_label = f" - Arguing for: {agent1_position}" if agent1_position else ""
                                    st.markdown(
                                        f'<div class="agent-1"><div class="agent-name">🔵 Agent Alpha (Logical & Analytical){position_label}</div>{latest_msg["content"]}</div>',
                                        unsafe_allow_html=True
                                    )
                                elif latest_msg["agent"] == "agent_2":
                                    position_label = f" - Arguing for: {agent2_position}" if agent2_position else ""
                                    st.markdown(
                                        f'<div class="agent-2"><div class="agent-name">🔴 Agent Beta (Passionate & Persuasive){position_label}</div>{latest_msg["content"]}</div>',
                                        unsafe_allow_html=True
                                    )
                        
                        # Show summary if available
                        if state.get("summary"):
                            with debate_container:
                                st.markdown("---")
                                st.markdown("### 🏆 Final Judgment & Summary")
                                st.markdown(
                                    f'<div class="judgment">{state["summary"]}</div>',
                                    unsafe_allow_html=True
                                )
            
            status_container.success("✅ Debate completed!")
            
            # Download option
            if st.button("💾 Download Debate Transcript"):
                transcript = f"# Debate: {topic}\n\n"
                for step_output in run_debate(topic, max_rounds, api_key):
                    for _, state in step_output.items():
                        if state.get("summary"):
                            transcript = state.get("history", "") + f"\n\n## Moderator's Summary\n{state['summary']}"
                
                st.download_button(
                    "Download",
                    transcript,
                    file_name=f"debate_{topic[:30]}.md",
                    mime="text/markdown"
                )
        
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.exception(e)

else:
    # Welcome message when no debate is running
    st.info("👆 Enter a topic and click 'Start Debate' to begin!")
    
    st.markdown("---")
    st.markdown("### 💡 Sample Topics to Try:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - Is remote work better than office work?
        - Should social media be regulated?
        - Is climate change the biggest threat?
        """)
    
    with col2:
        st.markdown("""
        - Should AI replace human teachers?
        - Is cryptocurrency the future of money?
        - Should space exploration be prioritized?
        """)
