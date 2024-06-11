from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from candidate import Candidate
import os


def instantiate_llm():
    model_name = "gpt-3.5-turbo-instruct"
    temperature = 0.0
    model = OpenAI(model_name=model_name, temperature=temperature, max_tokens=600)
    parser = PydanticOutputParser(pydantic_object=Candidate)

    prompt = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    return model, prompt