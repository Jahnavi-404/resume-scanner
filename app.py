import streamlit as st
import os
import PyPDF2
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to compute similarity
def calculate_similarity(resume_text, jd_text):
    documents = [resume_text, jd_text]
    cv = CountVectorizer().fit_transform(documents)
    similarity = cosine_similarity(cv[0:1], cv)
    return round(similarity[0][1]*100, 2)

# Streamlit UI
st.title("📄 AI-Powered Resume Scanner")
st.write("Upload resumes and match them with the job description.")

# Upload Job Description
jd_text = open("job_description.txt", "r").read()

# Upload Resumes
uploaded_files = st.file_uploader("Upload Resume PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    results = []
    for file in uploaded_files:
        resume_text = extract_text_from_pdf(file)
        score = calculate_similarity(resume_text, jd_text)
        results.append({"Candidate Name": file.name, "Match (%)": score})

    df = pd.DataFrame(results).sort_values(by="Match (%)", ascending=False)
    st.subheader("📊 Results")
    st.dataframe(df)
