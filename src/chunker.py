from langchain_text_splitters import RecursiveCharacterTextSplitter


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