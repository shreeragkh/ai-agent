import sys
from unittest.mock import MagicMock
import importlib.util


try:
    import torchvision
    from torchvision.transforms.v2 import functional
except Exception:
    for pkg in ["torchvision", "torchvision.ops", "torchvision.transforms", "torchvision.transforms.v2", "torchvision.io"]:
        mock = MagicMock()
        mock.__path__ = []
        mock.__spec__ = importlib.util.spec_from_loader(pkg, None)
        sys.modules[pkg] = mock

import streamlit as st
import os
from agent.graph import build_graph

# Page configuration
st.set_page_config(
    page_title="AutoStream AI Agent",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for premium look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    h1 {
        color: #00ffcc;
        text-align: center;
        font-family: 'Inter', sans-serif;
    }
    .status-box {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #00ffcc;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 AutoStream AI Agent")
st.markdown("---")

# Initialize graph in session state
if "app" not in st.session_state:
    with st.spinner("Initializing AI Agent..."):
        st.session_state.app = build_graph()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize agent state
if "agent_state" not in st.session_state:
    st.session_state.agent_state = {
        "user_input": "",
        "intent": None,
        "response": None,
        "name": None,
        "email": None,
        "platform": None
    }

# Sidebar for status
with st.sidebar:
    st.header("📊 Lead Status")
    state = st.session_state.agent_state
    
    if state.get("name") or state.get("email") or state.get("platform"):
        st.markdown(f"""
        <div class="status-box">
            <b>Name:</b> {state.get('name') or '---'}<br>
            <b>Email:</b> {state.get('email') or '---'}<br>
            <b>Platform:</b> {state.get('platform') or '---'}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No lead details captured yet.")
    
    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.session_state.agent_state = {
            "user_input": "",
            "intent": None,
            "response": None,
            "name": None,
            "email": None,
            "platform": None
        }
        st.rerun()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How can I help you today?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare input for the graph
    current_state = st.session_state.agent_state
    current_state["user_input"] = prompt

    # Invoke graph
    with st.spinner("Agent is thinking..."):
        try:
            new_state = st.session_state.app.invoke(current_state)
            st.session_state.agent_state = new_state
            
            response = new_state["response"]
            
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Trigger lead capture success toast if lead is captured
            if "✅ You're all set!" in response:
                st.balloons()
                st.success("Lead captured successfully!")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

    st.rerun()
