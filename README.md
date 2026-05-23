# 📄 RAG PDF Assistant

A production-ready AI-powered PDF question-answering system that lets users upload any PDF and ask natural language questions about it. Built with a clean separation between backend and frontend, using Retrieval Augmented Generation (RAG) to ground Claude's answers in the actual document content.

---

## What Is RAG?

RAG stands for Retrieval Augmented Generation. Instead of relying solely on an LLM's training data, the system first retrieves the most relevant parts of your document and passes them as context to the model. This significantly reduces hallucinations and ensures answers are grounded in your actual content.

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend API | FastAPI | Fast, async, production-grade |
| Vector Database | ChromaDB | Local, no account needed, easy setup |
| LLM Orchestration | LangChain | Handles chunking, retrieval, and chain building |
| LLM | Claude (claude-sonnet-4) | Accurate, context-aware answers |
| Frontend | Streamlit | Clean chat UI with minimal code |
| PDF Parsing | PyPDF | Reliable text extraction from PDFs |
| Embeddings | ChromaDB MiniLM | No API key needed for embeddings |

---

## How It Works

```
User uploads PDF
      │
      ▼
FastAPI receives file
      │
      ▼
PyPDF loads and reads all pages
      │
      ▼
LangChain splits into 1000-char chunks (150 char overlap)
      │
      ▼
Chunks embedded and stored in ChromaDB vector store
      │
      ▼
User asks a question
      │
      ▼
ChromaDB retrieves top 5 most relevant chunks (semantic search)
      │
      ▼
Claude receives chunks as context and generates grounded answer
      │
      ▼
Answer returned with source page numbers
```

---

## Project Structure

```
rag-pdf-assistant/
├── backend/
│   └── main.py          # FastAPI app — /upload and /ask endpoints
├── frontend/
│   └── app.py           # Streamlit chat UI
├── requirements.txt     # All dependencies
└── README.md
```

---

## Setup & Running

### 1. Clone and install dependencies

```bash
git clone https://github.com/YOUR_USERNAME/rag-pdf-assistant.git
cd rag-pdf-assistant
pip install -r requirements.txt
pip install langchain-text-splitters
```

### 2. Start the FastAPI backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO: Uvicorn running on http://127.0.0.1:8000
```

### 3. Start the Streamlit frontend (new terminal)

```bash
cd frontend
streamlit run app.py
```

### 4. Open your browser

Go to `http://localhost:8501`

- Paste your Anthropic API key in the sidebar
- Upload any PDF
- Start asking questions

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Upload a PDF, chunk and embed it |
| POST | `/ask` | Ask a question about an uploaded PDF |
| GET | `/health` | Health check |

### Example `/ask` request

```json
{
  "collection_name": "my_document",
  "question": "What are the main findings?",
  "api_key": "sk-ant-..."
}
```

### Example `/ask` response

```json
{
  "answer": "The main findings include...",
  "source_pages": [2, 5, 8],
  "question": "What are the main findings?"
}
```

---

## Key Design Decisions

**Why chunk with overlap?** LLMs have a context window limit so the entire PDF cannot be passed at once. Overlapping chunks (150 chars) ensure no information is lost at chunk boundaries.

**Why return source pages?** Transparency matters in AI systems. Users can verify answers against the original document, which builds trust and catches errors.

**Why local ChromaDB?** For a portfolio project, local storage removes the need for cloud accounts and API keys. In production this would be replaced with Pinecone or Weaviate for scalability.

---

## Resume Bullet Points

- Built a RAG pipeline using LangChain, ChromaDB, and Claude to enable semantic question answering over uploaded PDFs, with source page attribution for answer transparency
- Designed a FastAPI backend with document ingestion, vector embedding, and retrieval endpoints supporting persistent multi-document sessions via ChromaDB
- Developed a Streamlit chat interface with session history and real-time streaming, applying a human-in-the-loop design pattern to keep AI responses grounded in source material
