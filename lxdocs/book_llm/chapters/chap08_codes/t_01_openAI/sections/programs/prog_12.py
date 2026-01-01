def build_context(docs):
    context =  "\n\n".join(doc.page_content for doc in docs)
    
    MAX_CHARS = 3000 # Context window limit
    if len(context) > MAX_CHARS:
        context = context[:MAX_CHARS]
    return context

context = build_context(retrived_vectorDB_docs)


def build_context_with_sources(docs):
    lines = [ ]
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "?")
        lines.append(
            f"[Source {i+1}: {source}, page {page}]\n{doc.page_content}"
        )
    return "\n\n".join(lines)

context = build_context_with_sources(retrived_vectorDB_docs)


prompt = f""" You are a helpful assistant.

Answer the question ONLY using the context below.
Include source numbers in your answer.
If the answer is not in the context, say:
"I dont know based on the provided document."
Context:
{context}
Question:
{question}
"""