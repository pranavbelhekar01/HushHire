import streamlit as st
import pandas as pd
import os
from connect_template import prompt_template
from dotenv import load_dotenv
import logging
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def strip_response(response):
    prefix = "Answer: "
    if response.startswith(prefix):
        return response[len(prefix):]
    else:
        return response
    
def main():

    # load_dotenv()  # This loads the environment variables from a .env file

    os.getenv('OPENAI_API_KEY')
    
    st.set_page_config(layout="wide", page_title="Hushh Connect🚀")
    st.header("Hushh Connect🚀")

    user_csv = st.file_uploader("Upload your CSV!", type="csv")


    if user_csv is not None:
            
        st.info("Ask away!")
        user_question = st.text_input("Your question")
        llm = OpenAI(model_name='gpt-3.5-turbo-instruct',temperature=0)
        prompt = PromptTemplate(template=prompt_template, input_variables=["question"])
        llm_chain = LLMChain(prompt=prompt, llm=llm)

        if user_question is not None and user_question != "":
            
            response = llm_chain.run(user_question)
            #st.success(response)

            stripped_response = response.replace("Answer: ", "")
            print(stripped_response)
            logging.info(f'STRIPPED RESPONSE: {str(stripped_response)}')
            try:
                write_response(user_csv=user_csv, response=stripped_response)
            except Exception as e:
                st.warning(f"An error occurred: {e}. Please try again :(")


    
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
