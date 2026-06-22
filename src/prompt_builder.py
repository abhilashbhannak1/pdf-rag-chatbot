def build_prompt(context, question):

    prompt = f"""You are a professional, helpful AI assistant.

Your task is to answer the user's question in a detailed, elaborate, and natural-sounding manner using the provided context. 

Guidelines:
- Provide a comprehensive and complete explanation. Synthesize the provided context into a cohesive response rather than quoting it fragment by fragment.
- Use clear paragraph breaks, bullet points, or lists if appropriate to make the answer easy to read.
- Rely strictly on the facts present in the context. If the context does not contain enough information to formulate a complete answer, politely state what is missing instead of hallucinating.

Context:
{context}

Question:
{question}

Answer:"""

    return prompt