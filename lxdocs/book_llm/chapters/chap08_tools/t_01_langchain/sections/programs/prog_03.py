from langchain_openai   import ChatOpenAI
from langchain.prompts  import PromptTemplate
from langchain.chains   import LLMChain

llm             =   ChatOpenAI(model="gpt-3.5-turbo")

pro_template    =   PromptTemplate(
                        input_variables=["topic", "level"],
                        template="Explain {topic} for a {level} learner."
                    )

chain           =   LLMChain( llm=llm, prompt=pro_template)
response        =   chain.run( topic="LangChain", level="beginner" )

print(response)