import os
import anthropic
from dotenv import load_dotenv
from backend.pdf_processor import query_collection

load_dotenv()

MODEL = "claude-sonnet-4-6"


def _get_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set. Add it to your .env file.")
    return anthropic.Anthropic(api_key=api_key)


def answer_question(collection_name: str, question: str) -> str:
    chunks = query_collection(collection_name, question)
    context = "\n\n---\n\n".join(chunks)

    message = _get_client().messages.create(
        model=MODEL,
        max_tokens=1024,
        system=(
            "You are a helpful assistant that answers questions strictly based on the "
            "provided PDF context. If the answer is not in the context, say so clearly."
        ),
        messages=[
            {
                "role": "user",
                "content": f"Context from the PDF:\n\n{context}\n\nQuestion: {question}",
            }
        ],
    )
    return message.content[0].text
