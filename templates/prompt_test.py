from langchain_core.prompts import PromptTemplate

template = """
Provide the capital city of the given country.

Country: ```{input_country}```
"""

prompt = PromptTemplate(template=template, input_variables=["input_country"])
prompt.save("prompt_test.json")