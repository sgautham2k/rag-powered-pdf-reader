from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.pdf_processor import pdf_to_collection
from backend.qa_engine import answer_question

app = FastAPI(title="PDF Reader API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    collection_name: str
    question: str


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")
    file_bytes = await file.read()
    try:
        collection_name = pdf_to_collection(file_bytes, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {"collection_name": collection_name, "filename": file.filename}


@app.post("/ask")
async def ask_question(body: AskRequest):
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    try:
        answer = answer_question(body.collection_name, body.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"answer": answer}


@app.get("/health")
def health():
    return {"status": "ok"}
