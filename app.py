import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="PDF Reader", page_icon="📄", layout="centered")
st.title("📄 PDF Reader with Claude")
st.caption("Upload a PDF and ask questions about its content.")

# ── Session state ────────────────────────────────────────────────────────────
if "collection_name" not in st.session_state:
    st.session_state.collection_name = None
if "filename" not in st.session_state:
    st.session_state.filename = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Sidebar: PDF upload ──────────────────────────────────────────────────────
with st.sidebar:
    st.header("Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file and uploaded_file.name != st.session_state.filename:
        with st.spinner("Processing PDF…"):
            response = requests.post(
                f"{BACKEND_URL}/upload",
                files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
            )
        if response.ok:
            data = response.json()
            st.session_state.collection_name = data["collection_name"]
            st.session_state.filename = uploaded_file.name
            st.session_state.messages = []
            st.success(f"Ready: **{uploaded_file.name}**")
        else:
            st.error(f"Upload failed: {response.json().get('detail', 'Unknown error')}")

    if st.session_state.filename:
        st.info(f"Active: **{st.session_state.filename}**")
        if st.button("Clear / Load new PDF"):
            st.session_state.collection_name = None
            st.session_state.filename = None
            st.session_state.messages = []
            st.rerun()

# ── Main: chat interface ─────────────────────────────────────────────────────
if not st.session_state.collection_name:
    st.info("Upload a PDF in the sidebar to get started.")
    st.stop()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask a question about the PDF…")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            response = requests.post(
                f"{BACKEND_URL}/ask",
                json={
                    "collection_name": st.session_state.collection_name,
                    "question": question,
                },
            )
        if response.ok:
            answer = response.json()["answer"]
        else:
            answer = f"Error: {response.json().get('detail', 'Unknown error')}"
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
