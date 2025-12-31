# Python pip packages   :   langchain, langchain-openai, faiss-cpu
# Env variable          :   OPENAI_API_KEY

from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from step9_1_prepare_data import documents

documents = [ # Simulated chunks (normally from PDF + chunking)
    Document(
        page_content="LangChain is a framework for building LLM applications.",
        metadata={"source": "intro.pdf", "page": 1}
    ),
    Document(
        page_content="It provides abstractions for prompts, memory, and tools.",
        metadata={"source": "intro.pdf", "page": 2}
    )
]

embedding_model =   OpenAIEmbeddings( model="text-embedding-3-small" )

vectorstore     =   FAISS.from_documents(documents=documents, embedding=embedding_model)

vectorstore.save_local("faiss_index")   # Vector store saved to disk

# Reload FAISS index
vectorstore = FAISS.load_local( "faiss_index", 
                                embedding_model, 
                                allow_dangerous_deserialization=True)

results = vectorstore.similarity_search( "What is LangChain", k=2 )

for i, doc in enumerate(results):
    print(doc.page_content,  doc.metadata)