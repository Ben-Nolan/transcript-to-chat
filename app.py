
import streamlit as st
from dotenv import load_dotenv

from utils.chunking import chunk_text
from utils.dialogs import overwrite_vectorstore_dialog
from utils.llm import get_rag_chain
from utils.vectorestore import create_vector_store, get_embedding_model
from utils.youtube import get_transcript_text

load_dotenv()
st.set_page_config(page_title="Youtube Rag Walkthrough", layout="wide")

if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None


# Main UI Layout
st.title("Transcript-to-Chat: An Interactive RAG Playground")
st.markdown("""
This app breaks down the **RAG (Retrieval-Augmented Generation)** process step-by-step.
            """)


tab1, tab2, tab3, tab4 = st.tabs(["1. Data Ingestion",
                                  "2. Chunking",
                                  "3. Embedding",
                                  "4. RAG Chat"])

with tab1:
    st.header("Step 1: Get the Transcript")
    video_url = st.text_input("Paste Youtube URL here:",
                              placeholder="https://www.youtube.com/watch?v...")
    if st.button("Fetch Transcript"):
        with st.spinner("Pulling Video Transcript..."):
            st.session_state.transcript, transcript_type = (
                get_transcript_text(video_url)
            )
            st.success("Transcript loaded! "
                       f"(Transcript created from {transcript_type})")

    if st.session_state.transcript:
        st.subheader("Edit/Review Transcript")
        st.session_state.transcript = st.text_area(
            "Clean up the text (if necessary) before chunking:",
            value=st.session_state.transcript,
            height=300
        )

with tab2:
    st.header("Step 2: Recursive Chunking")
    if not st.session_state.transcript:
        st.warning("Please fetch a transcript in Step 1 first!")
    else:
        st.markdown("Click on 'Chunk Text' to slice the transcript into chunks.")
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("Parameters")
            size = st.slider("Chunk Size", 100, 2000, 500,
                             help="Max characters per chunk")
            overlap = st.slider("Overlap", 0, 500, 50,
                                help="Characters to repeat between chunks")

            if st.button("Chunk Text"):
                st.session_state.chunks = chunk_text(st.session_state.transcript,
                                                     size,
                                                     overlap)
                st.success(f"Created {len(st.session_state.chunks)} chunks!")

        with col2:
            st.subheader("Visualization")
            if st.session_state.chunks:
                for i, chunk in enumerate(st.session_state.chunks[:3]):
                    color = "#eof2f1"
                    st.markdown(f"""
                        <div style="background-color:{color};
                        padding:10px;
                        border-radius:5px;
                        margin-bottom:10px;
                        border: 1px solid #ccc;">
                            <strong>Chunk {i+1}</strong><br>{chunk}
                        </div>
                    """, unsafe_allow_html=True)

                if len(st.session_state.chunks) > 3:
                    st.info(f"... and {len(st.session_state.chunks) - 3} more chunks.")

with tab3:
    st.header("Step 3: Embedding & Vector Storage")

    if not st.session_state.chunks:
        st.warning("Please chunk your transcript in Step 2 first!")
    else:
        st.info(("This step turns your text into 384-dimensional"
                 "vectors using 'all-MiniLM-L6-v2'."))
    
        if st.button("Generate Vector Store"):
            if st.session_state.vector_store is not None:
                overwrite_vectorstore_dialog(create_vector_store,
                                             st.session_state.chunks)
            else:
                with st.spinner("Transforming text into vectors..."):
                    st.session_state.vector_store = (
                        create_vector_store((st.session_state.chunks))
                        )
                    st.success("Vector Store Created!"
                               "Your transcript is now searchable!")
        
        if st.session_state.vector_store:
            st.subheader("What does a Vector look like?")
            sample_text = st.session_state.chunks[0][:50] + "..."
            st.write(f"**Text Chunk:** {sample_text}")

            model = get_embedding_model()
            sample_vector = model.embed_query(st.session_state.chunks[0])
            st.write(f"**Vector (first 10 dimensions of {len(sample_vector)}):**)")
            st.json(sample_vector[:10])

with tab4:
    st.header("Step 4: Chat with the Video")

    if not st.session_state.vector_store:
        st.warning("Please complete the previous steps first!")
    else:
        k_chunks = st.slider("K chunks to retrieve:", 1, 10, 3, help="Number of chunks")
        user_query = st.text_input("Ask a question about the video:")

        if user_query:
            chain = get_rag_chain(st.session_state.vector_store, k_chunks)

            with st.spinner("Retreiving an answer..."):
                docs = st.session_state.vector_store.similarity_search(user_query,
                                                                       k=k_chunks)

                with st.expander("View Retrieved Evidence"):
                    for i, doc in enumerate(docs):
                        st.markdown(f"**Chunk {i+1}:**\n{doc.page_content}")
                
                response = chain.invoke(user_query)
                st.markdown("### AI Response:")
                st.write(response)