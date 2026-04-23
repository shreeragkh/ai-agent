import re
from agent.intent import detect_intent
from agent.rag import retrieve_context
from agent.tools import mock_lead_capture
from agent.llm import call_claude


def intent_node(state):
    state["intent"] = detect_intent(state["user_input"])
    # Store the first query that triggered the flow (only if it looks like a real question)
    if state["intent"] in ["pricing", "high_intent"] and not state.get("original_query"):
        state["original_query"] = state["user_input"]
    return state


def greeting_node(state):
    # Check if the user input contains specific keywords that shouldn't be handled by a generic greeting
    personal_keywords = ["name", "email", "platform", "details", "info"]
    if any(k in state["user_input"].lower() for k in personal_keywords):
        # Fallback to rag if it looks like a question despite greeting intent
        return rag_node(state)
        
    state["response"] = "Hello! I'm the AutoStream AI assistant. How can I help you with our video services today?"
    return state


def rag_node(state):
    context = retrieve_context(state["user_input"])
    
    user_info = f"""
Captured User Info:
- Name: {state.get('name') or 'Not captured'}
- Email: {state.get('email') or 'Not captured'}
- Platform: {state.get('platform') or 'Not captured'}
"""

    prompt = f"""
Answer the user using ONLY the Context and Captured User Info provided below.
If the user asks about their own details (name, email, platform) or their status, you MUST use the Captured User Info.
If the information is "Not captured", politely inform the user that you don't have that specific detail yet.

{user_info}

Context:
{context}

User: {state['user_input']}
Assistant:"""

    state["response"] = call_claude(prompt)
    return state


def extract_details(state):
    text = state["user_input"]

    # Email extraction
    email_match = re.search(r'\S+@\S+\.\S+', text)
    if email_match:
        state["email"] = email_match.group()

    # Platform extraction
    platforms = ["youtube", "instagram", "tiktok", "facebook", "twitch", "linkedin", "twitter", "x"]
    for p in platforms:
        if p in text.lower():
            state["platform"] = p.capitalize() if p != "x" else "X (Twitter)"
            break

    # Name fallback via LLM
    if not state.get("name") and not email_match:
        if len(text.split()) == 1:
             state["name"] = text.capitalize()
        else:
            prompt = f"Extract only the name from: {text}. If no name is found, return 'None'."
            name = call_claude(prompt).strip()
            if name.lower() != "none" and len(name.split()) <= 3:
                state["name"] = name

    return state


def lead_node(state):
    if not state.get("name"):
        state["response"] = "Exciting! We'd love to help you get started. To begin, may I know your name?"
        return state

    if not state.get("email"):
        state["response"] = "Please provide your email."
        return state

    if not state.get("platform"):
        state["response"] = "Which platform do you create content on?"
        return state

    # FINAL CALL - Capture lead
    mock_lead_capture(state["name"], state["email"], state["platform"])
    
    # User said: "you dont need to gave the plan after u returns we will contact"
    state["response"] = "✅ You're all set! We'll contact you soon."
    
    # Clear original query for next time
    state["original_query"] = None

    return state