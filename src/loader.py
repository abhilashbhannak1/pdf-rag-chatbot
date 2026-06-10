from langchain_community.document_loaders import PyPDFLoader
def load_pdf(pdf_path: str):
    """
    Load PDF and return LangChain Document objects
    """

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()
    return documents
if __name__ == "__main__":
    docs = load_pdf("data/22211A0431_BHANNAK_ABHILASH_.pdf")

    print("Total Pages:", len(docs))
    print("\nFirst Page Content:")
    print(docs[0].page_content)

    print("\nMetadata:")
    print(docs[0].metadata)
