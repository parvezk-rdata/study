# Python pip packages   :   langchain, langchain-openai
# Env variable          :   OPENAI_API_KEY

from langchain_openai import ChatOpenAI

llm         =   ChatOpenAI( model = "gpt-3.5-turbo", temperature = 0.3 )

prompt      =   "Explain what an LLM is in one paragraph."

response    =   llm.invoke(prompt)

print(response.content)
