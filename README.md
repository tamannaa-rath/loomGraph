# LoomGraph 🚀

## Problem
Corporate onboarding is inefficient and non-personalized.

## Solution
LoomGraph uses AI to:
- extract skills from resumes
- detect suitable roles
- identify skill gaps
- generate personalized learning paths

## Features
- AI-powered skill extraction
- Role detection engine
- Skill gap analysis
- Readiness scoring
- Personalized roadmap generation

## Tech Stack
- FastAPI
- React
- Gemini API

## How it works
1. User inputs resume
2. System extracts skills
3. Matches with role
4. Identifies gaps
5. Generates roadmap

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/tamannaa-rath/loomGraph.git
cd loomGraph
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # For Windows
pip install -r requirements.txt

# Create a .env file inside the backend folder and add:
GOOGLE_API_KEY=your_api_key_here

# Run the backend server:
uvicorn main:app --reload
```
### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```
### 4. Open the App
- Frontend: http://localhost:3000
- Backend: http://127.0.0.1:8000

## Impact
- Reduces onboarding time
- Personalized learning
- Improves employee productivity

## Future Improvements
- Skill graph visualization
- Resume upload support
- User authentication
- Analytics dashboard
