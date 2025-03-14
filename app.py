from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from PIL import Image
import os
import pdf2image
import google.generativeai as genai
import io
import base64


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response= model.generate_content([input, pdf_content[0], prompt==prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## convert the pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                'mime_type': 'image/jpeg',
                'data': base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

## Streamlit app

st.set_page_config(page_title="ATS Resume Expert", page_icon="🔮", layout="wide")
st.header("ATS Tracking System")
input_text = st.text_area("Enter the job description", key = "input", height=100)
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
        text=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt)
        st.subheader(response)

