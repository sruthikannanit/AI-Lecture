import os, re
from openai import OpenAI
from dotenv import load_dotenv
from code_runner import run_code

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_code(text):
    return re.findall(r"```python(.*?)```", text, re.DOTALL)

def process_text(text):

    prompt = f"""
    Analyze lecture:

    1. Summary
    2. Detect type: Math / Programming / Lab

    IF Math:
    - Generate 25 MCQs
    - Each with answer + step-by-step solution

    IF Programming:
    - Generate 30 problems
    - Each with code and output

    IF Lab:
    - 2 programs
    - explanation
    - sample input/output
    - diagram (text)

    Content:
    {text}
    """

    res = client.responses.create(
    model="gpt-4o-mini",
    input=prompt
)

result = res.output_text

    # execute code
    codes = extract_code(result)
    for code in codes:
        output = run_code(code)
        result += f"\n\nExecuted Output:\n{output}"

    return {"result": result}