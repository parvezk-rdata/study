from langchain_openai   import ChatOpenAI
from langchain.prompts  import PromptTemplate
from langchain.chains   import LLMChain

temp_stm        =   "Explain {topic} for a {level} learner."
temp_var        =   ["topic", "level"]
pro_template    =   PromptTemplate( input_variables=temp_var , template= temp_stm )

llm             =   ChatOpenAI(model="gpt-3.5-turbo")
chain           =   LLMChain( llm=llm, prompt=pro_template)

response        =   chain.run( topic="LangChain", level="beginner" )
print(response)