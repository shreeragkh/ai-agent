from typing import TypedDict, Optional

class AgentState(TypedDict):
    user_input: str
    original_query: Optional[str]
    intent: Optional[str]
    response: Optional[str]
    name: Optional[str]
    email: Optional[str]
    platform: Optional[str]