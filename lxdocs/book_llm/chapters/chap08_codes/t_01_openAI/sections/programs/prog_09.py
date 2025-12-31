# Python pip packages   :   langchain, langchain-openai
# Env variable          :   OPENAI_API_KEY

from langchain_openai import OpenAIEmbeddings

def cosine_similarity(vec1, vec2):
    dot_product =   np.dot(vec1, vec2)
    product     =   np.linalg.norm(vec1) * np.linalg.norm(vec2)
    normalized  =  dot_product / product
    return normalized

# Example text chunks (like after chunking)
chunks = [
    "LangChain is used to build LLM applications.",
    "LangChain helps create applications using large language models.",
    "I like to play football."
]

# Create embedding model
embeddings_model = OpenAIEmbeddings( model="text-embedding-3-small" )

# Generate embeddings : List[List[float]]
embeddings = embeddings_model.embed_documents(chunks)

sim_1_2 = cosine_similarity(embeddings[0], embeddings[1])
print(sim_1_2)