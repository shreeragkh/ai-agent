from agent.llm import call_claude

def detect_intent(user_input: str) -> str:
    prompt = f"""
Classify the user's intent into ONE of these categories:
- greeting: Simple hello, hi, or general pleasantries.
- pricing: Questions about costs, money, plans, features, or how the service works.
- high_intent: Explicit signals that the user is READY TO BUY, sign up, or proceed.
- info_sharing: User is providing their name, email, or other contact details.
- personal_info: User is asking about their own details (e.g., "what is my name?", "tell me my details").

User: {user_input}

Return only the label.
"""

    
    personal_keywords = ["my name", "my email", "my platform", "my details", "who am i", "my info"]
    if any(k in user_input.lower() for k in personal_keywords):
        return "personal_info"

   
    if "@" in user_input.lower():
        return "info_sharing"
    
    
    platforms = ["youtube", "instagram", "tiktok", "facebook", "twitch", "linkedin"]
    if user_input.lower().strip() in platforms:
        return "info_sharing"

    
    common_keywords = ["hi", "hello", "hey", "pricing", "plans", "cost", "money", "buy", "start"]
    if len(user_input.split()) == 1 and user_input.lower() not in common_keywords:
        return "info_sharing"

    result = call_claude(prompt).lower().strip()

    if "greeting" in result:
        return "greeting"
    elif "personal" in result:
        return "personal_info"
    elif "high" in result:
        return "high_intent"
    elif "info" in result:
        return "info_sharing"
    elif "pricing" in result:
        return "pricing"
    else:
        return "pricing"