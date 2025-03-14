import streamlit as st
import os
import PyPDF2 as pdf
import google.generativeai as genai
import io


from dotenv import load_dotenv
load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response= model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    if uploaded_file is not None:
        pdf_reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
        return text
    else:
        raise FileNotFoundError("No file uploaded")
    

## Streamlit app

st.set_page_config(page_title="ATS Resume Expert", page_icon="🔮", layout="wide")
st.header("ATS Tracking System")
jd = st.text_area("Enter the job description", height=100)
uploaded_file = st.file_uploader("Upload a pdf file", type="pdf")


if uploaded_file is not None:
    st.write("File uploaded successfully")

submit = st.button("Tell me about the resume")

input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt)
        st.subheader(response)

