import streamlit as st
import requests
import json

# Set page config
st.set_page_config(
    page_title="AI Ethics Agent",
    page_icon="🤖",
    layout="wide"
)

# Ollama configuration
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "mistral"  # You can change this to llama2, neural-chat, etc.

# Check Ollama connection
@st.cache_resource
def check_ollama():
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome screen
st.title("🤖 Welcome to the AI Ethics Agent")
st.markdown("""
## Explore AI Ethics Through Conversation

This is your interactive companion for discussing and understanding complex AI ethics cases and dilemmas.

### What can we discuss?
- **Algorithmic Bias & Fairness** - How do we ensure AI systems treat everyone fairly?
- **Privacy & Data Protection** - How should personal data be handled responsibly?
- **Transparency & Explainability** - How can we make AI decisions understandable?
- **Accountability & Governance** - Who is responsible when things go wrong?
- **Real-world Case Studies** - Examine actual ethical challenges in AI deployment

### How to use this agent:
Simply ask questions or present AI ethics scenarios, and we'll explore them together through informed discussion and analysis.

---
""")

# Chat interface
st.subheader("💬 Chat with the AI Ethics Agent")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Check Ollama status
if not check_ollama():
    st.error("⚠️ Ollama is not running! Please start Ollama first.")
    st.info("""
    ### How to set up Ollama:
    1. Download Ollama from [ollama.ai](https://ollama.ai)
    2. Install and run it
    3. In your terminal, run: `ollama pull mistral` (or another model)
    4. Ollama will run on `http://localhost:11434`
    5. Refresh this page once Ollama is running
    """)
else:
    st.success("✅ Connected to Ollama")

# Chat input
if prompt := st.chat_input("Ask about AI ethics, present a dilemma, or discuss a case..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from Ollama
    try:
        # Prepare system message for AI Ethics context
        system_message = """You are an expert AI Ethics Agent specializing in discussing and analyzing ethical challenges in artificial intelligence. 
You provide thoughtful, balanced perspectives on AI ethics issues including bias, privacy, transparency, accountability, and real-world case studies.
Help users understand complex ethical dilemmas through clear explanations and nuanced discussion."""
        
        # Prepare messages for Ollama
        messages_for_ollama = [
            {"role": "system", "content": system_message}
        ]
        messages_for_ollama.extend(st.session_state.messages)
        
        # Call Ollama API
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": messages_for_ollama,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            assistant_message = result["message"]["content"]
        else:
            assistant_message = f"Error: {response.status_code}. Make sure Ollama is running and the model '{OLLAMA_MODEL}' is installed."
        
    except Exception as e:
        assistant_message = f"I encountered an error: {str(e)}. Please make sure Ollama is running at {OLLAMA_URL}"
    
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    with st.chat_message("assistant"):
        st.markdown(assistant_message)
