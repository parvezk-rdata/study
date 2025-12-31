from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader

list_txt_docs1  =   TextLoader("sample.txt").load()
list_pages      =   PyPDFLoader("sample.pdf").load()
list_txt_docs2  =   DirectoryLoader(  path="texts/", 
                                      glob="*.txt", 
                                      loader_cls=TextLoader ).load()

print(list_txt_docs1[0].page_content)
print(list_txt_docs1[0].metadata)


print("PDF FILE CONTENT:\n")
for doc in list_pages:
    print(doc.page_content)
    print(doc.metadata)