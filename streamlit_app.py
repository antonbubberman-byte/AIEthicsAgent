import streamlit as st

# Set page config
st.set_page_config(
    page_title="AI Ethics Agent",
    page_icon="🤖",
    layout="wide"
)

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

# Chat input
if prompt := st.chat_input("Ask about AI ethics, present a dilemma, or discuss a case..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add bot response (placeholder for now)
    response = """Thank you for your question! This is a placeholder response. 
    
I'm being enhanced with specific AI ethics knowledge and frameworks. Soon, I'll be able to provide detailed, nuanced responses to your questions about AI ethics cases and dilemmas."""
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
