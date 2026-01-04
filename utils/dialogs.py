import streamlit as st
from typing import Callable

from langchain_core.vectorstores import VectorStore

@st.dialog("⚠️ Overwrite Warning")
def overwrite_vectorstore_dialog(
    on_confirm_callback: Callable[[list[str]], VectorStore],
    data_chunks: list[str]
) -> None:
    st.write("A vector store already exists. Overwrite?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, Create New", type="primary"):
            with st.spinner("Transforming text into vectors..."):

                st.session_state.vector_store = on_confirm_callback(data_chunks)
                st.success("Vector Store Created! Your transcript is now searchable!")

            st.rerun()

    with col2:
        if st.button("Cancel"):
            st.rerun()
    