from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai
import ast
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

print("DEBUG KEY:", os.getenv("GOOGLE_API_KEY"))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# -------------------------------
# Data
# -------------------------------

roles = {
    "Software Engineer": ["Python", "DSA", "DBMS", "System Design"],
    "Data Analyst": ["SQL", "Excel", "Python", "Statistics"],
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "Math"]
}

# -------------------------------
# Input Model
# -------------------------------

class ResumeInput(BaseModel):
    resume_text: str

# -------------------------------
# Skill Extraction Function
# -------------------------------

def extract_skills(resume_text):
    try:
                
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        
        prompt = f"""
        Extract technical skills from this resume.
        Return ONLY a Python list like this: ["Python", "React", "AWS"]

        Resume:
        {resume_text}
        """
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        text = text.replace("```python", "").replace("```", "").strip()
        
        skills_list = ast.literal_eval(text)
        return skills_list
        
    except Exception as e:
        return f"ERROR: {str(e)}"


def detect_role(user_skills):
    best_role = None
    max_match = 0

    for role, role_skills in roles.items():
        match = len(set(user_skills) & set(role_skills))

        if match > max_match:
            max_match = match
            best_role = role

    return best_role

def skill_gap(user_skills, role):
    role_skills = roles[role]
    gap = list(set(role_skills) - set(user_skills))
    return gap

def readiness_score(user_skills, role):
    role_skills = roles[role]
    matched = len(set(user_skills) & set(role_skills))
    total = len(role_skills)

    score = (matched / total) * 100
    return round(score, 2)

def explain_decision(user_skills, role):
    role_skills = roles[role]
    matched = list(set(user_skills) & set(role_skills))
    missing = list(set(role_skills) - set(user_skills))

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "reason": f"You are suited for {role} because you match {len(matched)} key skills."
    }

def generate_learning_path(user_skills, role, gap):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        prompt = f"""
        A user has skills: {user_skills}
        Target role: {role}
        Missing skills: {gap}

        Create a personalized learning roadmap.
        Keep it structured like:

        1. Skill: ...
           - What to learn
           - Suggested resources (course/project)
           - Estimated time

        Keep it concise and practical.
        """

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"ERROR: {str(e)}"
# -------------------------------
# API Endpoint
# -------------------------------

@app.post("/analyze")
def analyze(data: ResumeInput):
    skills = extract_skills(data.resume_text)

    if isinstance(skills, str):
        return {"error": skills}

    role = detect_role(skills)
    gap = skill_gap(skills, role)
    score = readiness_score(skills, role)
    explanation = explain_decision(skills, role)
    roadmap = generate_learning_path(skills, role, gap)

    return {
        "skills": skills,
        "detected_role": role,
        "skill_gap": gap,
        "readiness_score": score,
        "explanation": explanation,
        "learning_path": roadmap
    }