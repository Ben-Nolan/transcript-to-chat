import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_core.vectorstores import VectorStore
from langchain_huggingface import HuggingFaceEmbeddings


@st.cache_resource(show_spinner=False)
def create_vector_store(chunks: list[str]) -> VectorStore:
    """
    Convert chunks into vectors and store them in an in-memory ChromaDB
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    vectore_store = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        collection_name="youtube_transcript"
    )

    return vectore_store