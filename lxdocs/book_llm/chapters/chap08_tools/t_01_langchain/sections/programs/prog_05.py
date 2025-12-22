from langchain_openai           import ChatOpenAI
from langchain.prompts          import PromptTemplate
from langchain.output_parsers   import StructuredOutputParser, ResponseSchema


llm             =   ChatOpenAI(temperature=0)

pro_template    =   PromptTemplate(
                        input_variables=["question"],
                        template="{question}"
                    )






schemas = [
    ResponseSchema(name="definition", description="Short definition"),
    ResponseSchema(name="use_case", description="Where it is used"),
    ResponseSchema(name="example", description="Simple example"),
]

parser = StructuredOutputParser.from_response_schemas(schemas)

prompt = PromptTemplate(
    template="""
Explain {topic}.

{format_instructions}
""",
    input_variables=["topic"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

response = llm.invoke(prompt.format(topic="LangChain"))

parsed_output = parser.parse(response.content)
print(parsed_output)


