import sys
import streamlit as st

st.write("Python version:", sys.version)

import streamlit as st
import PyPDF2
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import textstat
import re

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to calculate similarity
def calculate_similarity(resume_text, jd_text):
    documents = [resume_text, jd_text]
    cv = CountVectorizer().fit_transform(documents)
    similarity = cosine_similarity(cv[0:1], cv)
    return round(similarity[0][1] * 100, 2)

# Function to calculate TF-IDF match score
def calculate_match_score(resume_text, jd_text):
    documents = [resume_text, jd_text]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return round(cosine_sim[0][0] * 100, 2)

# Predefined skill sets for different roles
job_roles = {
    "Software Developer": ["Python", "Java", "C++", "Software Engineering", "Algorithms", "Data Structures", "Django", "Flask"],
    "Full Stack Developer": ["HTML", "CSS", "JavaScript", "Node.js", "React", "MongoDB", "Express", "MySQL", "REST API", "Docker"],
    "Associate Software Engineer": ["Java", "C#", "Object-Oriented Programming", "Git", "Agile", "Software Testing", "SQL"],
    "Data Analyst": ["Excel", "SQL", "Python", "Pandas", "Data Visualization", "Tableau", "Statistics", "Machine Learning", "Data Mining"]
}

# All skills to extract
all_skills = list(set(skill for skills in job_roles.values() for skill in skills))

# Extract skills from resume
def extract_skills(text):
    found_skills = [skill for skill in all_skills if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE)]
    return found_skills

# Match resume against each role
def match_resume_with_role(resume_text, jd_text, job_roles):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    
    results = {}

    for role, role_skills in job_roles.items():
        common_skills = set(resume_skills).intersection(set(role_skills))
        match_percentage = (len(common_skills) / len(role_skills)) * 100
        results[role] = {
            "Match (%)": round(match_percentage, 2),
            "Common Skills": list(common_skills)
        }

    return results

# Generate Word Cloud
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400).generate(text)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)

# Readability Score
def readability_score(resume_text):
    return textstat.flesch_reading_ease(resume_text)

# -------------------- STREAMLIT APP --------------------

st.title("📄 AI-Powered Resume Scanner")
st.write("Upload resumes and match them with the job description.")

# Upload job description
jd_text = open("job_description.txt", "r").read()

# Upload Resumes
uploaded_files = st.file_uploader("Upload Resume PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    results = []
    for file in uploaded_files:
        resume_text = extract_text_from_pdf(file)
        
        # Scores
        similarity = calculate_similarity(resume_text, jd_text)
        tfidf_score = calculate_match_score(resume_text, jd_text)
        readability = readability_score(resume_text)
        role_match_results = match_resume_with_role(resume_text, jd_text, job_roles)

        # Best-fit role (only for Best Fit Suggestion)
        best_role, best_data = max(role_match_results.items(), key=lambda x: x[1]["Match (%)"])

        # **For Overall Summary**: Remove Best Fit Role, and include only job description match details
        results.append({
            "Candidate Name": file.name,
            "Match (%)": similarity,
            "TF-IDF Match (%)": tfidf_score,
            "Readability Score": readability,
        })

        # Display Word Cloud
        st.subheader(f"📝 Word Cloud for {file.name}")
        generate_wordcloud(resume_text)

        # **Role Match Results** - Display how resume matches job description roles
        st.subheader(f"📊 Role Match Details for {file.name}")
        for role, data in role_match_results.items():
            st.write(f"**{role}**: {data['Match (%)']}% match")
            st.write(f"Common Skills: {', '.join(data['Common Skills']) if data['Common Skills'] else 'None'}")

        

    # **Final Table** (Job Description related only, no Best Fit Role)
    df = pd.DataFrame(results).sort_values(by="Match (%)", ascending=False)
    st.subheader("📊 Overall Summary (Job Description Related Only)")
    st.dataframe(df)

