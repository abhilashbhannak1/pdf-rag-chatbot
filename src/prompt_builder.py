def build_prompt(context, question):

    prompt = f"""
You are a helpful assistant.

Answer the question only from the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt