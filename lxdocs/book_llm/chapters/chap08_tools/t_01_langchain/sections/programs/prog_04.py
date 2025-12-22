from langchain_openai   import ChatOpenAI
from langchain.prompts  import PromptTemplate
from langchain.chains   import LLMChain
from langchain.memory   import ConversationBufferMemory


llm             =   ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
memory          =   ConversationBufferMemory()
pro_template    =   PromptTemplate(
                        input_variables=["question"],
                        template="{question}"
                    )
chain           =   LLMChain( llm=llm, prompt=pro_template, memory=memory)

response1       =   chain.run("What is LangChain?")
response2       =   chain.run("Give a simple example.")

