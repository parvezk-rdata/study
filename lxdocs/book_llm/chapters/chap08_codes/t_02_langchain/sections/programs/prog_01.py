# pip install langchain langchain-openai
# export OPENAI_API_KEY="your_api_key_here"
# echo 'export OPENAI_API_KEY="your_api_key_here"' >> ~/.bashrc

from langchain_openai import ChatOpenAI

# Create LLM object
llm         =   ChatOpenAI( model = "gpt-3.5-turbo", temperature = 0.3 )

# Send a prompt
prompt      =   "Explain what an LLM is in one paragraph."
response    =   llm.invoke(prompt)

# Print response
print(response.content)
