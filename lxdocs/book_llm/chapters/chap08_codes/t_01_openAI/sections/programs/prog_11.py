from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

embedding_model     =   OpenAIEmbeddings( model="text-embedding-3-small")

vectorstore         =   FAISS.load_local( "faiss_index", embedding_model,
                                          allow_dangerous_deserialization=True
                        )

query = "What is LangChain?"

# Top-K, Filtering by metadata, Without Scores
docs = vectorstore.similarity_search( query=query, k=2, 
                                      filter={"source": "intro.pdf"} 
        )

for i, doc in enumerate(docs):
    print(doc.page_content)
    print(doc.metadata)

# Top-K, Filtering by metadata
docs = vectorstore.similarity_search_with_score( query=query, k=2, 
                                      filter={"source": "intro.pdf"} 
        )

# Top-K, Filtering by metadata, With Scores
for i, (doc, score) in enumerate(docs):
    print(doc.page_content)
    print(score)