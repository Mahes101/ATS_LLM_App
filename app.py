import streamlit as st 
import google.generativeai as genai 
import os 
import PyPDF2

from dotenv import load_dotenv 
load_dotenv() 

import os

genai.configure(api_key = os.getenv("GOOGLE-API-KEY"))

#Get a gemini response
def get_gemini_response(input,jd):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(input)
    return response.text

def input_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()

    return text
        
# Prompt template
prompt = """
    Hey act like a skilled or experience ATS(Application Tracking System) recruiter with a deep understanding of
    tech field, software engineering, data science, data analyst, big data engineer, and machine learning. Your task is to 
    evaluate the resume based on the given job description. You must consider the job market is very competitive and you should 
    provide a best assistance for improving the resumes. Assign the percentage matching based on JD and the missing keywords 
    with high accuracy.
    resume: {text}
    job description: {job_description}
    
    I want the response in single string having the structure:
    {{"JD matching percentage": "%", "Missing Keywords : []","Profile Summary ": " "}}
    """    

#Streamlit App
st.set_page_config(page_title="Smart ATS", page_icon=":robot_face:", layout="wide")

st.title("Improve Resume with Smart ATS ")
jd = st.text_area("Enter Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="PDF files only")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_from_pdf(uploaded_file)
        #prompt = prompt.format(text=text, job_description=jd)
        response = get_gemini_response(prompt,text)
        st.subheader("The Response is:")
        st.write(response)
    
    