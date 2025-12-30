# Transcript-to-Chat: An Interactive RAG Playground

This application provides a hands-on visualization of the RAG (Retrieval-Augmented Generation) lifecycle. By using a YouTube URL as a dynamic data source, you can navigate the engineering pipeline step-by-step:

1. **Data Ingestion**: Extract raw, unstructured transcript data from the YouTube API.
2. **Transformation (Chunking)**: Implement recursive character splitting to segment the text into semantically dense chunks, balancing context vs. precision.
3. **Vectorization**: Generate embeddings to map text into a high-dimensional mathematical space where semantic similarity can be calculated.
4. **Indexing**: Initialize an in-memory vector database (ChromaDB) to house and query your transcript embeddings.
5. **Inference**: Prompt the LLM! Observe how the model retrieves relevant "evidence" from your vector store to generate a grounded response.
6. **Evaluation & Iteration**: Go back and tune parameters like Chunk Size and Overlap to see how they impact the quality and accuracy of the AI's output.

<br>

[Link to Streamlit App](https://transcript-to-chat-pbzjqwpjhnfzxedlyt3hf8.streamlit.app/)

<br>

# Why RAG?
A significant hurdle in deploying Large Language Models (LLMs) is their knowledge cutoff. LLMs are trained on massive public datasets, but they lack access to an organization's private or real-time data. For example, while a model may know general information about a company, it cannot answer a customer’s question about a specific purchase because that data wasn't in its training set.

Retrieval-Augmented Generation (RAG) solves this by allowing an organization to "ground" the LLM in proprietary data. Instead of relying on its memory, the model acts as an intelligent search engine, pulling information based on a given prompt from a "library" (the vector-store) of internal information and documents provided to the model.

About this App:
This application demonstrates a complete RAG pipeline using a YouTube transcript as the data source (content the model has possibly never "seen" before). Users can interact with each stage of the process:

- Ingestion: Pulling raw data via API.
- Transformation: Chunking text for semantic density.
- Retrieval: Finding the most relevant context using Vector Search.
- Generation: Observing how the LLM uses that retrieved context to provide a factual, grounded response.

<br>

# Technology Stack:
*   **Language:** [Python 3.12](https://www.python.org/)
*   **UI:** [Streamlit](https://streamlit.io/)
*   **Framework:** [LangChain](https://python.langchain.com/)
*   **Inference:** [Groq Cloud](https://groq.com/) (Llama 3 8B)
*   **Vector Database:** [ChromaDB](https://www.trychroma.com/)
*   **Embeddings:** `all-MiniLM-L6-v2` (Sentence-Transformers)
*   **Environment:** [Poetry](https://python-poetry.org/)

<br>

# Quick setup (for local development)

### Prerequisites
*   Python 3.12
*   Poetry
*   A Groq API Key (Free at [console.groq.com](https://console.groq.com))

### 1. Clone the repository
```bash
git clone https://github.com/ben-nolan/transcript-to-chat.git
cd transcript-to-chat
```

### 2. Install Dependencies
```bash
poetry install
```

### 3. Set API Key
- Acquire an API key via [console.groq.com](https://console.groq.com)
- Follow instructions in .streamlit/secrets.toml.example file to set API key

### 4. Run the Application
```bash
poetry run streamlit run app.py
```

### Testing & Linting
```bash
# Run Tests
poetry run pytest

# Run Linter
poetry run ruff check .

# Run type checker
poetry run mypy .
```

<br>

# Future Improvements
There are many additions that could be added to the app. Here are a couple I'm working on for the future:

- **RAGAS Evaluation**: Provide real-time feedback on the relevancy of the LLM's reponse
- **Visual Updates**: Add visual elements to communicate impact of chosen parameter values
    - e.g. highlight overlapping text to show how much of each chunk is overlapped text
