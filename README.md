# AutoStream AI Agent 🤖

AutoStream is an intelligent lead-generation agent designed for video services. It uses RAG (Retrieval-Augmented Generation) and a structured state machine to capture leads before providing detailed service and pricing information.

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone <repository-url>
cd auto-stream-agent
```

### 2. Set Up Environment
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure API Keys
Create a `.env` file in the root directory and add your Anthropic API key:
```env
ANTHROPIC_API_KEY=your_api_key_here
```

### 4. Run the Application
Start the Streamlit interface:
```bash
streamlit run streamlit_app.py
```

---

## 🏗️ Architecture Explanation

### Why LangGraph?
For this project, I chose **LangGraph** over AutoGen because it provides superior control over the conversational flow. While AutoGen excels at open-ended multi-agent collaboration, AutoStream requires a structured, deterministic path to ensure business logic is followed (e.g., capturing a lead's contact info before disclosing pricing). LangGraph allows me to define a **cyclic graph** where each node represents a specific functional block—Intent Detection, RAG Retrieval, or Lead Extraction. This "flow-as-code" approach makes the agent's behavior predictable, easy to debug, and highly reliable for lead-generation workflows.

### How State is Managed
State is managed using a centralized **State Schema** (based on Python's `TypedDict`). As a user interacts with the agent, the state object is passed between nodes, accumulating information along the way. For example:
1. The **Intent Node** identifies if the user is sharing info.
2. The **Extraction Node** parses the name/email and updates the state.
3. The **Lead Node** checks the state for missing fields before allowing the flow to proceed to RAG.
In the Streamlit frontend, this LangGraph state is bridged with `st.session_state` to ensure the sidebar and chat history stay perfectly in sync with the agent's internal memory.

## 🧠 Model Information

This project uses **Claude 4.5 Haiku** (`claude-haiku-4-5-20251001`) for its advanced reasoning and efficient processing of agent intents.

### Troubleshooting: Why am I getting a 404 Error?
If you attempt to use older models, you may encounter an **Anthropic 404 error**. 

In this environment, **Claude 3 series models are returning 404 errors** as they have been superseded by the Claude 4 series. Ensure that `agent/llm.py` is configured to use a supported Claude 4 model identifier.

**Current Valid Model:**
- `claude-haiku-4-5-20251001`

## 📱 WhatsApp Deployment

To deploy this agent on WhatsApp, I would use the **Meta WhatsApp Business API** with a dedicated Webhook server.

### Integration Steps:
1.  **Webhook Setup:** I would build a lightweight **FastAPI** or **Flask** server to host a `/webhook` endpoint. This endpoint would receive real-time HTTP POST notifications from Meta whenever a user sends a message.
2.  **Request Processing:** The server would extract the `sender_id` (phone number) and the `message_body`. 
3.  **State Persistence:** Since WhatsApp is asynchronous, I would integrate a **PostgreSQL or Redis Checkpointer** into LangGraph. This allows the agent to retrieve the correct conversation state using the user's phone number as the unique key.
4.  **Responding:** Once the LangGraph agent processes the message and generates a response, the server would send an authorized POST request back to the WhatsApp Business API to deliver the reply to the user.
5.  **Multimodal Support:** If users send images or videos, the webhook would download the media from the Meta CDN, and we could extend the LangGraph nodes to process these using Vision models.
