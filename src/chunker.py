from langchain_text_splitters import RecursiveCharacterTextSplitter

from loader import load_pdf


def create_chunks(documents):
    """
    Split documents into chunks
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    return chunks
if __name__ == "__main__":

    docs = load_pdf("data/22211A0431_BHANNAK_ABHILASH_.pdf")

    chunks = create_chunks(docs)

    print("Total Chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\n{'='*60}")
    print(f"CHUNK {i+1}")
    print(f"{'='*60}")

    print(chunk.page_content)

    print("\nMetadata:")
    print(chunk.metadata)