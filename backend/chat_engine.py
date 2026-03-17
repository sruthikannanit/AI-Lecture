import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

history = []

def chat_with_video(q, ctx):
    global history

    history.append({"role": "user", "content": q})
res = client.responses.create(
    model="gpt-4o-mini",
    input=ctx + "\n\nUser: " + q
)

ans = res.output_text
   
    history.append({"role":"assistant","content":ans})

    return {"answer": ans}