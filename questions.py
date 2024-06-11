from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import PyPDF2
import google.generativeai as genai
import re

app = FastAPI()

# Configure Google Generative AI
genai.configure(api_key="AIzaSyA6cT3ZpL2WM0vxVct5CC6a8Ok6GeWnpy0")

# Function to extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

# Function to generate interview questions
def generate_questions(job_description, resume):
    prompt = f"""This is a job description {job_description} \n Here's a resume of a candidate applying for this role: \n {resume} \n Based on the information provided, write a list of interview questions to assess the candidate's suitability for the role.
    Interview questions should be innovative and level of hardness should be decided based the position and requirements required for the job role
    Output format of generation should strictly follow the following rules:
    a. Output should contain only the list of questions, nothing else (no description and no purpose of question)
        Example: 
        output should be: 
        1. question1
        2. question2
        3. question3
        output should not be:
        1. question1 (to test technical knowledge)
        2. question2 (to test technical knowledge)
        3. question3 (to test technical knowledge)
    b. should contain the variety of questions- technical, logical, problem solving, puzzles(if necessary), etc
    c. questions should be exact 3 in number
    d. ask the questions relevant to the resume that is provided above. example: Projects, skills, experience, etc
    e. questions must be in accordance of job requirement
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    questions = response.text
    questions_list = [question.strip() for question in questions.strip().split('\n') if question]
    questions_list = [re.sub(r'^\d+\.\s*', '', question) for question in questions_list]
    return questions_list

# Function to evaluate answers
def evaluate_answer(question, answer):
    prompt = f""" 
    Assume yourself as an interviewer who is analyzing the answers of the candidate. Give the score to the question out of 10. check the facts before giving the score to the candidate. keep the evaluation short. 
    Question: {question}
    Answer: {answer}
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    score = response.text.strip()
    return score

@app.post("/upload/")
async def upload_files(job_description: str, resume: UploadFile = File(...)):
    try:
        text = await resume.read()
        resume_text = extract_text_from_pdf(text)
        questions = generate_questions(job_description, resume_text)
        return JSONResponse(content={"questions": questions}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/evaluate/")
async def evaluate_answers(question: str, answer: str):
    try:
        score = evaluate_answer(question, answer)
        return JSONResponse(content={"score": score}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
