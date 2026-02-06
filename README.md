# 🧠 Knowledge Copilot

**Description:**  
A personal AI assistant that remembers your conversations, helps answer questions, and can be augmented with external knowledge in the future (RAG-ready).

**Features:**  
- Google Authentication  
- Persistent chat memory in SQL  
- Timestamps for messages  
- Context window (last N messages sent to AI)  
- Developer mode & debug panel  
- Reset chat & logout functionality  
- Frontend with Streamlit  
- Backend with FastAPI + Groq LLM  

**Installation & Running:**  
1. Clone the repo:  
   ```bash
   git clone https://github.com/<your-username>/knowledge-copilot.git
   
2. Navigate to project:
   ```bash
   cd knowledge-copilot

3. Create virtual environment:

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


4. Install dependencies:

pip install -r requirements.txt


5. Set up .env with:

GROQ_API_KEY=<your-api-key>
GOOGLE_CLIENT_ID=<your-google-client-id>
GOOGLE_CLIENT_SECRET=<your-google-client-secret>
MODEL=<groq-model-name>


6. Run backend:

uvicorn backend.main:app --reload


7. Run frontend:

streamlit run frontend/app.py
