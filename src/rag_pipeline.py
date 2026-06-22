import os
from typing import List, Tuple
from langchain_core.documents import Document
from src.loader import load_pdf
from src.chunker import create_chunks
from src.embeddings import get_embeddings
from src.vectorstore import create_vectorstore
from src.retriever import create_retriever
from src.llm_model import get_llm
from src.prompt_builder import build_prompt

class RagPipeline:
    def __init__(self):
        self.embeddings = get_embeddings()
        self.llm = get_llm()
        self.vectorstore = None
        self.retriever = None

    def initialize_with_pdf(self, pdf_path: str) -> int:
        """
        Loads a PDF, chunks it, creates a vector store, and sets up the retriever.
        Returns the total number of chunks.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found at {pdf_path}")
        
        # Load PDF
        documents = load_pdf(pdf_path)
        
        # Create Chunks
        chunks = create_chunks(documents)
        
        # Create Vector Store
        self.vectorstore = create_vectorstore(chunks, self.embeddings)
        
        # Create Retriever
        self.retriever = create_retriever(self.vectorstore)
        
        return len(chunks)

    def query(self, question: str) -> Tuple[str, List[Document]]:
        """
        Queries the RAG pipeline. Returns (answer, list_of_retrieved_documents).
        """
        if not self.retriever:
            raise ValueError("Pipeline not initialized. Please call initialize_with_pdf first.")
            
        # Retrieve relevant chunks
        results = self.retriever.invoke(question)
        
        # Combine retrieved chunks into context
        context = "\n\n".join([doc.page_content for doc in results])
        
        # Build prompt
        prompt = build_prompt(context, question)
        
        # Generate response
        response = self.llm.invoke(prompt)
        
        return response.content, results

if __name__ == "__main__":
    # Test execution
    pipeline = RagPipeline()
    pdf_path = "data/22211A0431_BHANNAK_ABHILASH_.pdf"
    if os.path.exists(pdf_path):
        num_chunks = pipeline.initialize_with_pdf(pdf_path)
        print(f"Initialized with {num_chunks} chunks.")
        
        question = "What is Abhilash's CGPA?"
        answer, docs = pipeline.query(question)
        print(f"Question: {question}")
        print(f"Answer: {answer}")
        print("Sources:")
        for idx, doc in enumerate(docs, 1):
            print(f"Source {idx}: (Page {doc.metadata.get('page', 'unknown')}) - {doc.page_content[:100]}...")
    else:
        print(f"Test PDF not found at {pdf_path}")
