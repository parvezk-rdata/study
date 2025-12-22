# pip install langchain langchain-openai
# export OPENAI_API_KEY="your_api_key_here"
# echo 'export OPENAI_API_KEY="your_api_key_here"' >> ~/.bashrc

from langchain_openai   import ChatOpenAI
from langchain.prompts  import PromptTemplate

temp_stm        =   "Explain {topic} for a {level} learner."
temp_var        =   ["topic", "level"]
pro_template    =   PromptTemplate( input_variables=temp_var , template= temp_stm )
final_prompt    =   pro_template.format( topic="LangChain", level="beginner" )

llm             =   ChatOpenAI(model="gpt-3.5-turbo")
response        =   llm.invoke(final_prompt)

print(response.content)
