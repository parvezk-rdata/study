from langchain.text_splitter import RecursiveCharacterTextSplitter
from sample_text import text

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""] 
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i+1} ---")
    print(chunk)
