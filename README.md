# PDF RAG Chatbot

A Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions based on their content. The system extracts text from PDFs, creates embeddings, stores them in a vector database, retrieves relevant context, and generates accurate responses using a Large Language Model (LLM).

## Features

* Upload PDF documents
* Extract and process PDF text
* Generate embeddings for semantic search
* Store document vectors in a vector database
* Ask questions about uploaded PDFs
* Context-aware answer generation using RAG
* Simple and interactive user interface

## Project Structure

```text
pdf-rag-chatbot/
│
├── app.py
├── src/
├── data/
├── requirements
├── README.md
└── .gitignore
```

## Tech Stack

* Python
* LangChain
* FAISS / Vector Database
* OpenAI / LLM Integration
* PDF Processing Libraries

## Installation

1. Clone the repository

```bash
git clone https://github.com/abhilashbhannak1/pdf-rag-chatbot.git
```

2. Navigate to the project folder

```bash
cd pdf-rag-chatbot
```

3. Create a virtual environment

```bash
python -m venv .venv
```

4. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

5. Install dependencies

```bash
pip install -r requirements
```

## Usage

Run the application:

```bash
python app.py
```

Upload a PDF and start asking questions about its content.

## Future Enhancements

* Multi-PDF support
* Chat history memory
* Improved retrieval techniques
* Streamlit/FastAPI deployment
* Source citation support

## Author

Abhilash Bhannak
