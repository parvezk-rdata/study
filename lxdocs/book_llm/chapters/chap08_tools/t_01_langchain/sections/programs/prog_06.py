from langchain_openai 	import ChatOpenAI
from langchain.tools 	import tool

@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression"""
    return str(eval(expression))

@tool
def read_file(file_name: str) -> str:
    """Reads a text file and returns its content"""
    with open(file_name, "r") as f:
        return f.read()


llm		=   ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools 	=   llm.bind_tools([read_file, calculator])

prompt		=   "Use the file reading tool to summarize notes.txt"
response 	=   llm_with_tools.invoke(prompt)

print(response)


# LLM sees Tool's name, description, parameters