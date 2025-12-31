from langchain_openai           import ChatOpenAI
from langchain.prompts          import PromptTemplate
from langchain.output_parsers   import StructuredOutputParser, ResponseSchema

schemas = [
                ResponseSchema(name="definition", description="Short definition"),
                ResponseSchema(name="use_case", description="Where it is used"),
                ResponseSchema(name="example", description="Simple example"),
]

parser          =   StructuredOutputParser.from_response_schemas(schemas)
format_instrn   =   parser.get_format_instructions()
var_map         =   { "format_instructions": format_instrn}
temp_stm        =   """
                        Explain {topic}.

                        {format_instructions}
                    """
temp_var        =   ["topic"]

pro_template    =   PromptTemplate( template = temp_stm, 
                                    input_variables = temp_var, 
                                    partial_variables = var_map)

final_prompt    =   pro_template.format( topic="LangChain" )

llm             =   ChatOpenAI(temperature=0)
response        =   llm.invoke(final_prompt)
parsed_output   =   parser.parse(response.content)
print(parsed_output)


