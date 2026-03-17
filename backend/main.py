from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from lecture_detector import is_lecture

import google.generativeai as genai

# 🔑 Configure your API key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-pro")

app = FastAPI()

# ✅ Global storage for video content
VIDEO_DATA = ""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 Request models
class RequestData(BaseModel):
    text: str
    title: str

class ChatData(BaseModel):
    question: str


# 🔥 ANALYZE API (MAIN FEATURE)
@app.post("/analyze")
def analyze(data: RequestData):

    global VIDEO_DATA

    # ✅ Store transcript
    VIDEO_DATA = data.text

    # ✅ Check if lecture
    if not is_lecture(data.text, data.title):
        return {"result": "❌ Not a lecture video"}

    # 🧠 AI Tutor Prompt
    prompt = f"""
    You are an AI tutor.

    Lecture content:
    {VIDEO_DATA}

    Perform the following:

    1. Give a clear summary.

    2. Identify lecture type:
    - maths
    - theory
    - lab
    - electronics

    3. Based on type:

    IF maths:
    - Generate 20 problems
    - Provide step-by-step solutions

    IF theory:
    - Generate 30 MCQ questions with answers

    IF lab:
    - Give sample readings
    - Explain experiment clearly
    - Describe diagram step-by-step

    IF electronics:
    - Generate MCQs
    - Explain circuits
    - Describe circuit diagrams clearly

    IMPORTANT:
    Use ONLY the lecture content.
    Do NOT use outside knowledge.
    """

    response = model.generate_content(prompt)

    return {"result": response.text}


# 🔥 CHAT (ASK QUESTIONS)
@app.post("/chat")
def chat(data: ChatData):

    global VIDEO_DATA

    # ❌ If no analyze done
    if VIDEO_DATA == "":
        return {"answer": "⚠️ Please click Analyze first."}

    # 🧠 Context-based answering
    prompt = f"""
    Answer ONLY from this lecture:

    {VIDEO_DATA}

    Question:
    {data.question}
    """

    response = model.generate_content(prompt)

    return {"answer": response.text}step 4 5 6 