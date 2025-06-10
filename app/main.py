from fastapi import Request, FastAPI
import os
from fastapi.responses import JSONResponse
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY= os.environ.get("AI_API_KEY")

if not API_KEY:
    raise RuntimeError("AI_API_KEY is not set in the environment or .env file")

app = FastAPI()
client = genai.Client(api_key=API_KEY)


@app.get("/")
def root():
    return {"message from server":"Hello World!"}

@app.post("/generate-manim")
async def generateManim(request: Request):

    payload = await request.json()
    concept = payload.get("concept")
    
    response =  client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""
                        You are an expert in Manim (Mathematical Animation Engine). You are an expert at using Manim (Mathematical Animation Engine). Your task is to generate highly accurate, syntactically valid Manim code in Python that creates a clear, animated explanation of the concept described after the --- separator. Generate fully valid, executable Python code for a Manim animation based strictly on the official documentation: https://docs.manim.community

                        Strict Instructions:
                        - Start with `from manim import *`.
                        - Define a class named `Animation` inheriting from a Scene subclass (e.g., `Scene`, `MovingCameraScene`, etc.).
                        - Python code can contain explanations, if specified by user (as part of the animation itself, but should be non intrusive and non-overlapping)
                        - Implement a `construct(self)` method with complete animation logic.
                        - Do NOT include comments, markdown, or text outside the code.
                        - Do NOT use `.rotate()` on NumPy arrays like `UP`, `DOWN`, or results from `.get_center()`. Use `rotate_vector(vec, angle)` instead.
                        - Do NOT assume external files, media, or SVGs. Use only Manim primitives.
                        - The output must be completely self-contained, error-free, and ready to run.

                        Return **only the Python code**. No explanations, no markdown, no prose.

                        ---
                        {concept}""",
        ).text
    with open("test.py", "w") as f:
        f.write(response)

    return JSONResponse(status_code=200, content=response)
