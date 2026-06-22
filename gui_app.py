# pyrefly: ignore [missing-import]
import streamlit as st
import os
import shutil
from src.rag_pipeline import RagPipeline

# Page config
st.set_page_config(
    page_title="Premium PDF RAG Chatbot",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling
st.markdown("""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main Background & Accent Colors */
    .stApp {
        background-color: #0E1117;
        color: #E2E8F0;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1A1F2C;
        border-right: 1px solid #2D3748;
    }
    
    /* Title glow effect */
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #38BDF8, #818CF8, #34D399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        text-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #94A3B8;
        margin-bottom: 2rem;
    }
    
    /* Card design for UI widgets */
    div.stAlert {
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        background-color: rgba(30, 41, 59, 0.7);
    }
    
    /* Custom buttons */
    .stButton>button {
        background: linear-gradient(135deg, #4F46E5, #06B6D4);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5);
        color: white;
    }
    
    /* Source box styling */
    .source-card {
        background-color: #1E293B;
        border-left: 4px solid #38BDF8;
        padding: 12px;
        margin-bottom: 12px;
        border-radius: 0 8px 8px 0;
        border-top: 1px solid rgba(255,255,255,0.05);
        border-right: 1px solid rgba(255,255,255,0.05);
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    
    .source-meta {
        font-weight: bold;
        color: #38BDF8;
        font-size: 0.85rem;
        margin-bottom: 6px;
    }
    
    .source-text {
        font-style: italic;
        font-size: 0.9rem;
        color: #CBD5E1;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        color: #64748B;
        font-size: 0.85rem;
    }
    
    /* Quick styling rules */
    hr {
        border-color: rgba(255, 255, 255, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pipeline" not in st.session_state:
    st.session_state.pipeline = None
if "current_pdf_name" not in st.session_state:
    st.session_state.current_pdf_name = None
if "num_chunks" not in st.session_state:
    st.session_state.num_chunks = 0

# Sidebar configuration
with st.sidebar:
    st.image("https://img.icons8.com/clouds/100/pdf.png", width=70)
    st.title("Settings & Upload")
    st.markdown("---")
    
    # PDF File uploader
    uploaded_file = st.file_uploader(
        "Upload a PDF Document", 
        type=["pdf"], 
        help="Select a PDF document to chunk, index, and ask questions about."
    )
    
    # Process uploaded file
    if uploaded_file is not None:
        file_name = uploaded_file.name
        
        # If a new file is uploaded
        if st.session_state.current_pdf_name != file_name:
            with st.spinner(f"Processing '{file_name}'... Chunking and embedding..."):
                try:
                    # Create data directory if it doesn't exist
                    os.makedirs("data", exist_ok=True)
                    
                    # Save the uploaded file
                    pdf_path = os.path.join("data", file_name)
                    with open(pdf_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Initialize/Rebuild the RAG Pipeline
                    pipeline = RagPipeline()
                    chunks_count = pipeline.initialize_with_pdf(pdf_path)
                    
                    # Update session state
                    st.session_state.pipeline = pipeline
                    st.session_state.current_pdf_name = file_name
                    st.session_state.num_chunks = chunks_count
                    st.session_state.messages = []  # Reset chat history for new doc
                    
                    st.success("Vector Store generated successfully!")
                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")
    else:
        # If no file uploaded, reset state
        if st.session_state.current_pdf_name is not None:
            st.session_state.pipeline = None
            st.session_state.current_pdf_name = None
            st.session_state.num_chunks = 0
            st.session_state.messages = []

    # Display document statistics
    if st.session_state.current_pdf_name:
        st.markdown("### Document Stats")
        st.info(f"📄 **Active File:** {st.session_state.current_pdf_name}\n\n✂️ **Chunks Created:** {st.session_state.num_chunks}")
        
        # Reset chat button
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    else:
        st.warning("⚠️ Please upload a PDF to initialize the search engine.")
        
    st.markdown("---")
    st.markdown("### Model Details")
    st.text("LLM: Llama 3.3 (70B) via Groq")
    st.text("Embeddings: all-MiniLM-L6-v2")
    st.text("API Key: Configured (.env)")

# Main Panel
st.markdown("<h1 class='main-title'>📄 PDF RAG Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Ask questions based on your uploaded PDF documents. The model will only reply using context from the document.</p>", unsafe_allow_html=True)

# Check if pipeline is initialized
if st.session_state.pipeline is None:
    st.info("👋 **Welcome!** Upload a PDF document in the sidebar to get started. The application will read the text, divide it into segments, convert them into vector embeddings, and store them locally in a FAISS vector store. Once initialized, you can chat with the document contents.")
else:
    # Display Chat Messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
            # Show sources if any
            if msg["role"] == "assistant" and msg.get("sources"):
                with st.expander("🔍 View Retrieved Sources"):
                    for idx, doc in enumerate(msg["sources"], 1):
                        page = doc.metadata.get("page", 0) + 1  # 0-indexed to 1-indexed for reader
                        st.markdown(f"""
                            <div class='source-card'>
                                <div class='source-meta'>Source {idx} - Page {page}</div>
                                <div class='source-text'>"{doc.page_content}"</div>
                            </div>
                        """, unsafe_allow_html=True)

    # Chat Input
    if question := st.chat_input("Ask a question about the uploaded document..."):
        # User message
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
            
        # Assistant response
        with st.chat_message("assistant"):
            with st.spinner("Retrieving document sections and generating answer..."):
                try:
                    answer, docs = st.session_state.pipeline.query(question)
                    
                    st.write(answer)
                    
                    # Display sources in expander
                    with st.expander("🔍 View Retrieved Sources"):
                        for idx, doc in enumerate(docs, 1):
                            page = doc.metadata.get("page", 0) + 1
                            st.markdown(f"""
                                <div class='source-card'>
                                    <div class='source-meta'>Source {idx} - Page {page}</div>
                                    <div class='source-text'>"{doc.page_content}"</div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                    # Save assistant message to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": docs
                    })
                except Exception as e:
                    st.error(f"Error querying pipeline: {str(e)}")

# Footer
st.markdown("""
    <div class='footer'>
        PDF RAG Chatbot • Built with Streamlit, LangChain, FAISS & Groq Llama 3.3
    </div>
""", unsafe_allow_html=True)
