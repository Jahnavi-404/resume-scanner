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

# Function to calculate match score based on keywords
def calculate_match_score(resume_text, jd_text):
    documents = [resume_text, jd_text]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Use the cosine_similarity function from sklearn
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])  # Compare the first document (resume) with the second (JD)
    
    # Return the similarity score as a percentage
    return round(cosine_sim[0][0] * 100, 2)

# Predefined skill sets for different roles
job_roles = {
    "Software Developer": ["Python", "Java", "C++", "Software Engineering", "Algorithms", "Data Structures", "Django", "Flask"],
    "Full Stack Developer": ["HTML", "CSS", "JavaScript", "Node.js", "React", "MongoDB", "Express", "MySQL", "REST API", "Docker"],
    "Associate Software Engineer": ["Java", "C#", "Object-Oriented Programming", "Git", "Agile", "Software Testing", "SQL"],
    "Data Analyst": ["Excel", "SQL", "Python", "Pandas", "Data Visualization", "Tableau", "Statistics", "Machine Learning", "Data Mining"]
}

# Function to extract skills from text
def extract_skills(text):
    all_skills = ["Python", "Java", "C++", "C#", "JavaScript", "HTML", "CSS", "SQL", "Machine Learning", "Django", "Flask", "React", "Node.js", "MongoDB", "Excel", "Pandas", "Tableau", "Git", "Agile", "Software Testing", "Data Structures", "Algorithms", "Docker", "REST API", "MySQL"]
    found_skills = [skill for skill in all_skills if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE)]
    return found_skills

# Function to match resume with job roles
def match_resume_with_role(resume_text, jd_text, job_roles):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    
    results = {}

    # Iterate over job roles and calculate match percentage
    for role, role_skills in job_roles.items():
        common_skills = set(resume_skills).intersection(set(role_skills))
        match_percentage = (len(common_skills) / len(role_skills)) * 100
        results[role] = {"Match (%)": round(match_percentage, 2), "Common Skills": common_skills}

    return results

# Function to generate a word cloud
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400).generate(text)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)

# Function to calculate readability score
def readability_score(resume_text):
    score = textstat.flesch_reading_ease(resume_text)
    return score

# Streamlit UI
st.title("📄 AI-Powered Resume Scanner")
st.write("Upload resumes and match them with the job description.")

# Upload Job Description (can be uploaded as text or loaded from a file)
jd_text = open("job_description.txt", "r").read()

# Upload Resumes
uploaded_files = st.file_uploader("Upload Resume PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    results = []
    for file in uploaded_files:
        resume_text = extract_text_from_pdf(file)
        
        # Calculate similarity and match scores
        score = calculate_similarity(resume_text, jd_text)
        match_score = calculate_match_score(resume_text, jd_text)
        readability = readability_score(resume_text)
        
        # Get job role match results
        role_match_results = match_resume_with_role(resume_text, jd_text, job_roles)
        
        results.append({"Candidate Name": file.name, "Match (%)": score, "Match Score (%)": match_score, "Readability Score": readability})

        # Display word cloud for resume
        st.subheader(f"📝 Word Cloud for {file.name}")
        generate_wordcloud(resume_text)
        
        # Display job role match results
        st.subheader(f"📝 Role Match Results other than JD {file.name}")
        for role, result in role_match_results.items():
            st.write(f"**{role}**: {result['Match (%)']}% Match")
            st.write(f"Common Skills: {', '.join(result['Common Skills'])}")
    
    df = pd.DataFrame(results).sort_values(by="Match (%)", ascending=False)
    st.subheader("📊 Results for Job Description")
    st.dataframe(df)
