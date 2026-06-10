"""from src.loader import load_pdf
from src.chunker import create_chunks

pdf_path = "data/22211A0431_BHANNAK_ABHILASH_.pdf"

documents = load_pdf(pdf_path)

chunks = create_chunks(documents)

print("Total Documents:", len(documents))
print("Total Chunks:", len(chunks))

print("\nChunk 1:\n")
print(chunks[0].page_content)

print("\nChunk 1 Metadata:\n")
print(chunks[0].metadata)


print(chunks[0].page_content)

print("\n=================\n")

print(chunks[1].page_content)

print("\n=================\n")

print(chunks[2].page_content)
print("\n=================\n")

print(chunks[3].page_content)

print("\n=================\n")

print(chunks[4].page_content) 

from src.embeddings import get_embeddings

embeddings = get_embeddings()

vector = embeddings.embed_query(
    "Python is easy to learn"
)

print(type(vector))

print(len(vector))

print(vector[:10]) 



from src.loader import load_pdf
from src.chunker import create_chunks
from src.embeddings import get_embeddings
from src.vectorstore import create_vectorstore

pdf_path = "data/22211A0431_BHANNAK_ABHILASH_.pdf"

documents = load_pdf(pdf_path)

chunks = create_chunks(documents)

embeddings = get_embeddings()

vectorstore = create_vectorstore(
    chunks,
    embeddings
)

print("Vector Store Created Successfully")
print("Total Chunks:", len(chunks))



#4
from src.loader import load_pdf
from src.chunker import create_chunks
from src.embeddings import get_embeddings
from src.vectorstore import create_vectorstore
from src.retriever import create_retriever

pdf_path = "data/22211A0431_BHANNAK_ABHILASH_.pdf"

documents = load_pdf(pdf_path)

chunks = create_chunks(documents)

embeddings = get_embeddings()

vectorstore = create_vectorstore(
    chunks,
    embeddings
)

retriever = create_retriever(
    vectorstore
)

query = "What is Abhilash's CGPA?"
query = "What technologies were used in Skill Synch?"

results = retriever.invoke(query)

print("Retrieved Chunks:\n")

for i, doc in enumerate(results, 1):
    print(f"\n===== Chunk {i} =====\n")
    print(doc.page_content)  """

# 5

from src.loader import load_pdf
from src.chunker import create_chunks
from src.embeddings import get_embeddings
from src.vectorstore import create_vectorstore
from src.retriever import create_retriever
from src.llm_model import get_llm
from src.prompt_builder import build_prompt

# Load PDF
pdf_path = "data/22211A0431_BHANNAK_ABHILASH_.pdf"

documents = load_pdf(pdf_path)

# Create Chunks
chunks = create_chunks(documents)

# Load Embedding Model
embeddings = get_embeddings()

# Create Vector Store
vectorstore = create_vectorstore(
    chunks,
    embeddings
)

# Create Retriever
retriever = create_retriever(
    vectorstore
)

# Load LLM
llm = get_llm()

print("=" * 50)
print("📄 PDF RAG Chatbot Started")
print("Type 'exit' to quit")
print("=" * 50)

# Chat Loop
while True:

    question = input("\nAsk Question: ")

    if question.lower() == "exit":
        print("\n👋 Goodbye!")
        break

    # Retrieve Relevant Chunks
    results = retriever.invoke(question)

    # Combine Retrieved Chunks into Context
    context = "\n\n".join(
        [doc.page_content for doc in results]
    )

    # Build Prompt
    prompt = build_prompt(
        context,
        question
    )

    # Generate Response
    response = llm.invoke(prompt)

    print("\nAnswer:")
    print(response.content)