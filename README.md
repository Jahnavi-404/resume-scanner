AI POWERED RESUME SCANNER

This project is an AI-powered resume scanner that extracts text from resumes in PDF format and compares them with predefined job descriptions. The application calculates match scores using cosine similarity and TF-IDF, analyzes the readability of resumes, visualizes common skills between resumes and job descriptions, and generates word clouds from the resume text.


FEATURES

PDF Resume Upload: Upload resumes in PDF format.

Job Description Comparison: Compares uploaded resumes with a job description to calculate match percentages.

Cosine Similarity: Measures the similarity between the resume and job description.

TF-IDF Matching: Provides an advanced comparison using the TF-IDF algorithm.

Skill Extraction & Match: Extracts skills from resumes and compares them against predefined skill sets for various roles (e.g., Software Developer, Full Stack Developer).

Readability Score: Evaluates the readability of the resume using the Flesch Reading Ease score.

Word Cloud: Visualizes the most frequent words from the resume text using a word cloud.


TECHNOLOGIES USED

Python 3.12: The programming language used to build the application.

Streamlit: Framework used for building the interactive web interface.

PyPDF2: Library for extracting text from PDF files.

scikit-learn: Used for calculating cosine similarity and TF-IDF scores.

WordCloud: For generating word cloud visualizations.

Matplotlib: For displaying the word cloud.

textstat: For calculating the readability of the resume text.

pandas: For organizing and displaying results in tabular form.

re (Regular Expressions): For skill extraction and matching.


INSTALLATION

1. Clone the Repository

git clone https://github.com/Jahnavi-404/resume-scanner.git
cd resume-scanner

2. Install the Dependencies

pip install -r requirements.txt

3. Run the Application

streamlit run app.py

4. Upload Resumes

Once the app is running, you can upload PDF resumes and compare them against a predefined job description. The results will include:

Similarity percentage

TF-IDF match percentage

Readability score

Skills match with predefined roles

Word cloud visualization of the resume text


HOW IT WORKS

PDF Upload: Upload PDF files containing resumes.

Comparison: The uploaded resume is compared with a predefined job description.

Results: The app calculates the similarity, TF-IDF match, and readability scores. It also shows a list of common skills between the resume and job description and displays a word cloud of the resume text.




