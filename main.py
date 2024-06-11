import os
import sys
import csv
import json
from typing import List, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from PyPDF2 import PdfReader
from langchain.callbacks import get_openai_callback
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
import pandas as pd
import logging

from src.rank import extract_and_rank
from src.candidate import Candidate
from src.llm_config import instantiate_llm
from src.template import prompt_template

app = FastAPI()

def extract_resume(resume):
    reader = PdfReader(resume)
    return "".join(page.extract_text() for page in reader.pages)

@app.post("/upload_resumes/")
async def upload_resumes(files: List[UploadFile] = File(...), no_of_resumes: int = Form(...), job_description: str = Form(...)):
    if len(job_description) < 25:
        raise HTTPException(status_code=400, detail="Invalid or Empty job description! Please make sure your job description has at least 25 characters!")

    dict_object = {}
    rows = []
    resumes = [file.file for file in files]
    ranked_resumes, embeddings_bank, text_bank = extract_and_rank(resumes, job_description)

    no_of_resumes = int(no_of_resumes)
    model, prompt = instantiate_llm()

    for selected_resume in ranked_resumes[:no_of_resumes]:
        resume_text = text_bank[selected_resume[0]]
        doc_query = f"Return only a json based on this candidate's resume information: {resume_text}"
        input = prompt.format_prompt(query=doc_query)

        parser = PydanticOutputParser(pydantic_object=Candidate)

        with get_openai_callback() as cb:
            try:
                result = model(input.to_string())
                class_object = parser.parse(result)
                dict_object = class_object.__dict__
                rows.append(dict_object)
            except Exception as error:
                logging.error(error)

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
    return df.to_dict(orient="records")

def write_csv(user_csv, field_names, rows):
    with open(user_csv, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def write_response(user_csv, response: str):
    df = pd.read_csv(user_csv)
    data = eval(response)
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
