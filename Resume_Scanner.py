import os
import PyPDF2
from difflib import SequenceMatcher

#setting the resumes folder path
folder_path=r"C:\Users\chodi\OneDrive\Desktop\Resumes"

#here im giving some skills set and i can expand this later for different job roles
skills_set=["python", "java", "c", "c++", "c#", "javascript", "typescript",
    "machine learning", "deep learning", "nlp", "data analysis", "data analytics", "data visualization", "statistics",
    "pandas", "numpy", "matplotlib", "scikit", "tensorflow", "keras",
    "git", "github", "docker", "kubernetes", "linux",
    "aws", "azure", "gcp",
    "html", "css", "react", "node", "flask", "django",
    "mysql", "sql", "postgres", "mongodb",
    "communication", "problem solving", "teamwork", "leadership"]

def reading_pdf_text(pdf_path):
    text=""
    with open(pdf_path,"rb") as f:
        reader=PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text=page.extract_text()
            if page_text:
                text+=page_text
    return text.lower()

def extract_jd_keywords(jd_text):
    jd_text=jd_text.lower()
    found=[]
    for skill in skills_set:
        if skill in jd_text:
            found.append(skill)
    return set(found)

def similarity(a,b):
    return SequenceMatcher(None,a,b).ratio()

def compare_resume_to_jd(jd_keywords,resume_text):
    matched_skills=set()
    missed_skills=set()
    words=resume_text.split()
    for keyword in jd_keywords:
        found=False
        for word in words:
            if(similarity(keyword,word)>0.75):
                matched_skills.add(keyword)
                found=True
                break
        if not found:
            missed_skills.add(keyword)
    score=(len(matched_skills)/len(jd_keywords))*100 if jd_keywords else 0
    return matched_skills,missed_skills,round(score,2)
job_desc=input("Enter the job description here: ")
jd_keywords=extract_jd_keywords(job_desc)
for file_name in os.listdir(folder_path):
    if file_name.endswith(".pdf"):
        resume_path=os.path.join(folder_path,file_name)
        print(f"\n Checking resume: {file_name}")

        resume_text=reading_pdf_text(resume_path)
        matched_skills,missed_skills,score=compare_resume_to_jd(jd_keywords,resume_text)
        print("Matched Skills are: ",matched_skills)
        print("Missed Skills are: ",missed_skills)
        print("Match score is: ",score,"%")
print("\nAll resumes processed!")