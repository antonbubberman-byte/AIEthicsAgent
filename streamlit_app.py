import streamlit as st
import requests
import json
import os

# Set page config
st.set_page_config(
    page_title="AI Ethics Agent",
    page_icon="🤖",
    layout="wide"
)

# Hugging Face Inference API configuration
HF_API_KEY = st.secrets.get("HF_API_KEY", os.getenv("HF_API_KEY"))
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"  # Open-source model
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

# Check Hugging Face API key
@st.cache_resource
def check_hf_connection():
    if not HF_API_KEY:
        return False, "No API key"
    try:
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        response = requests.get("https://huggingface.co/api/user", headers=headers, timeout=5)
        if response.status_code == 200:
            return True, "Connected"
        else:
            return False, f"Invalid API key (status {response.status_code})"
    except Exception as e:
        return False, str(e)

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

# Check Hugging Face connection status
is_connected, status_msg = check_hf_connection()

if not HF_API_KEY:
    st.error("⚠️ Hugging Face API Key not found!")
    st.info("""
    ### How to set up Hugging Face Inference API:
    1. Go to [huggingface.co](https://huggingface.co) and create a free account
    2. Generate an API key in your account settings
    3. Create a `.streamlit/secrets.toml` file in your project with:
       ```
       HF_API_KEY = "your-api-key-here"
       ```
    4. Or set the environment variable: `export HF_API_KEY="your-api-key-here"`
    5. Refresh this page after adding the API key
    """)
elif not is_connected:
    st.error(f"⚠️ Connection Error: {status_msg}")
else:
    st.success("✅ Connected to Hugging Face Inference API")

# Chat input
if HF_API_KEY and is_connected:
    if prompt := st.chat_input("Ask about AI ethics, present a dilemma, or discuss a case..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response from Hugging Face
        try:
            # Prepare system message for AI Ethics context
            system_message = """You are an expert AI Ethics Agent specializing in discussing and analyzing ethical challenges in artificial intelligence. 
You provide thoughtful, balanced perspectives on AI ethics issues including bias, privacy, transparency, accountability, and real-world case studies.
Help users understand complex ethical dilemmas through clear explanations and nuanced discussion."""
            
            # Format messages for the model
            conversation_text = system_message + "\n\n"
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    conversation_text += f"User: {msg['content']}\n"
                else:
                    conversation_text += f"Assistant: {msg['content']}\n"
            
            conversation_text += "Assistant: "
            
            # Call Hugging Face API
            headers = {"Authorization": f"Bearer {HF_API_KEY}"}
            response = requests.post(
                HF_API_URL,
                headers=headers,
                json={
                    "inputs": conversation_text,
                    "parameters": {
                        "max_new_tokens": 500,
                        "temperature": 0.7,
                    }
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    assistant_message = result[0].get("generated_text", "").replace(conversation_text, "").strip()
                else:
                    assistant_message = "Error: Unexpected response format"
            else:
                assistant_message = f"Error: {response.status_code}. {response.text}"
            
        except Exception as e:
            assistant_message = f"I encountered an error: {str(e)}"
        
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
