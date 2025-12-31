# Python pip packages   :   langchain, langchain-openai
# Env variable          :   OPENAI_API_KEY

from langchain_openai   import ChatOpenAI
from langchain.prompts  import PromptTemplate

temp_stm        =   "Explain {topic} for a {level} learner."
temp_var        =   ["topic", "level"]
pro_template    =   PromptTemplate( input_variables=temp_var , template= temp_stm )

final_prompt    =   pro_template.format( topic="data structures", level="beginner" )
llm             =   ChatOpenAI(model="gpt-3.5-turbo")

response        =   llm.invoke(final_prompt)

print(response.content)
