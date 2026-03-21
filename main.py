from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai
import ast


load_dotenv()

print("DEBUG KEY:", os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

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
                
        model = genai.GenerativeModel("gemini-flash-latest")
        
        prompt = f"""
        Extract technical skills from this resume.
        Return ONLY a Python list like this: ["Python", "React", "AWS"]

        Resume:
        {resume_text}
        """
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean markdown if present (same as your original)
        text = text.replace("```python", "").replace("```", "").strip()
        
        # Your preferred ast.literal_eval
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

    return {
        "skills": skills,
        "detected_role": role,
        "skill_gap": gap,
        "readiness_score": score,
        "explanation": explanation
    }