import os
import sys
import csv
import json
import streamlit as st
from PyPDF2 import PdfReader
from langchain.callbacks import get_openai_callback
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
import pandas as pd
import logging

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from rank import extract_and_rank
from candidate import Candidate
from llm_config import instantiate_llm
from template import prompt_template

def extract_resume(resume):
    reader = PdfReader(resume)
    return "".join(page.extract_text() for page in reader.pages)


def main():
    st.set_page_config(layout="wide", page_title="Hushh Jobs")
    st.header("Hushh Jobs 💼")
    model, prompt = instantiate_llm()
    col1, col2 = st.columns(2)

    with col1:
        resumes = st.file_uploader(
            "Upload resumes here!", accept_multiple_files=True, type="pdf"
        )
        no_of_resumes = st.number_input("Enter the number of resumes you want to shortlist",step=1)


    with col2:
        job_description = st.text_area("Enter the job description here!", height=250)
        rank_btn = st.button("Rank")
       

    
    
    
    

    if resumes and rank_btn:

        if len(job_description) < 1:
            st.warning(
                "Invalid or Empty job description! Please make sure your job description has atleast 25 characters!"
            )

        else:
            dict_object = {}
            rows = []
            ranked_resumes, embeddings_bank, text_bank = extract_and_rank(
                resumes, job_description
            )

            no_of_resumes=int(no_of_resumes)
            for selected_resume in ranked_resumes[:no_of_resumes]:
                resume_text = text_bank[selected_resume[0]]

                doc_query = f"Return only a json based on this candidate's resume information: {resume_text}"
                input = prompt.format_prompt(query=doc_query)

                #using PydanticOutputParser for structuring language model responses into a coherent, JSON-like format.
                parser = PydanticOutputParser(pydantic_object=Candidate)

                with get_openai_callback() as cb:
                    try:
                        result = model(input.to_string())
                        # st.success(result)
                        class_object= parser.parse(result)  #using the above defined pydantic output parser to structure the response in a json-format
                        dict_object=class_object.__dict__
                        #dict_object = json.loads(result)
                        rows.append(dict_object)
                    except Exception as error:
                        print(error)
            field_names = [
                "name",
                "email",
                "phone",
                "location",
                "degree",
                "college",
                "skills",
                "companies",
                "roles",
                "degree_year",
                "experience",
            ]
            user_csv = "shortlisted.csv"
            write_csv(user_csv=user_csv, field_names=field_names, rows=rows)
            df = pd.read_csv(user_csv)
            st.dataframe(df)


#def write_csv(user_csv, field_names, rows):
def write_csv(user_csv, field_names, rows):
    with open(user_csv, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_response(user_csv, response: str):
    """
    Write a response from an agent to a Streamlit app.

    Args:
        response_dict: The response from the agent.

    Returns:
        None.
    """

    df = pd.read_csv(user_csv)
    data = eval(response)
    st.dataframe(data=data, use_container_width=True)


if __name__ == "__main__":
    main()