from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embeddings
if __name__ == "__main__":
    embeddings = get_embeddings()

    text = "Python is a programming language."

    vector = embeddings.embed_query(text)

    print("Text:", text)
    print("Vector Length:", len(vector))
    print("First 10 Values:", vector[:10])