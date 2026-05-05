# Dual-Agent Debate System

**Course**: CSE601 Computational Thinking  
**Authors**: Jyoti Triklani (AU2544015) & Gautam Prajapati (AU2544033)  
**Institution**: Ahmedabad University, SEAS

## Overview

The **Dual-Agent Debate System** is an AI-powered matchmaking and debate orchestration platform. It is designed to tackle the issues in current debate platforms by pairing two distinctive AI agents—one logical and one emotional—to argue over user-provided topics. The system utilizes **LangGraph** to coordinate back-and-forth multi-round arguments, with **Google Gemini 2.0 Flash** performing the generation, and evaluated by an impartial AI moderator.

### The Debaters
- **🔵 Agent Alpha**: Logical & Analytical. Uses factual data, evidence-based reasoning, and structured logic.
- **🔴 Agent Beta**: Passionate & Persuasive. Relies on emotional appeals, real-world examples, and persuasive human-centric rhetoric.
- **🟣 Moderator**: Offers automated fair judgment and summarized conclusions after max rounds are reached.

## Features
- **Automatic Position Assignment**: Specifically detects "vs" formulations (e.g., "Hardwork vs Talent") and strictly assigns explicit sides to Agent Alpha and Beta.
- **Multi-Round Exchanging**: A fully managed round-by-round conversation flow implemented using **LangGraph**.
- **Interactive UI**: An elegant Streamlit interface that streams agent responses and displays final evaluations.
- **Transcript Downloads**: Download out-of-the-box debate transcripts in Markdown formatting.

## Architecture & Tech Stack

This project maps directly to computational thinking pillars (Decomposition, Pattern Recognition, Abstraction, and Algorithm Design) and relies on:
- **Python 3.13+**
- **Streamlit**: Real-time Interactive Web UI
- **LangGraph**: State Management & Core Agent Workflow Orchestration 
- **Google Generative AI (Gemini API)**: LLM backends tailored with varied temperature profiles per agent.

### System Flow
1. **User Input** $\rightarrow$ Streamlit initiates session.
2. **LangGraph Workflow Init** $\rightarrow$ Sets topic, state, and `max_rounds`.
3. Agent Alpha formulates initial pro-claim.
4. Agent Beta counters.
5. Loop iterates until `current_round > max_rounds`.
6. AI Moderator reviews history and rules a Final Judgment/Summary.

## Installation

1. Clone or download this project to your local machine.
2. Ensure you have Python installed.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your API key:
   - Create a `.env` file in the root directory.
   - Insert your Google Gemini API key:
     ```
     GOOGLE_API_KEY="your_api_key_here"
     ```
   - *Alternatively, you can provide the API key directly via the Streamlit web sidebar.*

## Usage

Start the Streamlit application using:
```bash
streamlit run app.py
```

Once running:
1. Provide your configured **Google Gemini API Key** in the sidebar.
2. Adjust the number of max debate rounds.
3. Enter a Topic under "Enter Debate Topic" (e.g., *Is remote work better than office work?* or *Hardwork vs Talent*).
4. Click **Start Debate** and watch the AI agents argue! 

## Directory Structure
- `app.py`: Streamlit main execution point and UI definitions.
- `agents/`: Contains debate agents construction module and specific argument prompts.
- `graph/`: Contains the LangGraph workflow structures and debate state tracking.
- `ppt/`: Contains the LaTeX (`.tex`) presentation for the academic coursework.
- `report/`: Contains the LaTeX report for the project.

## Note
This project leverages `models/gemini-2.0-flash` ensuring high-speed processing ideal for responsive app experiences. Time delays are intrinsically added between prompts to safeguard from API rate limits.