from langchain_openai   import ChatOpenAI
from langchain.prompts  import PromptTemplate
from langchain.chains   import LLMChain
from langchain.memory   import ConversationBufferMemory

temp_stm        =   "{question}"
temp_var        =   ["question"]
pro_template    =   PromptTemplate( input_variables=temp_var , template= temp_stm )

llm             =   ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
memory          =   ConversationBufferMemory()
chain           =   LLMChain( llm=llm, prompt=pro_template, memory=memory)

response1       =   chain.run(question="What is LangChain?")
response2       =   chain.run(question="Give a simple example.")

