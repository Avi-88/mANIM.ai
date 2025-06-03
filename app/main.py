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
                        You are an expert at using Manim (Mathematical Animation Engine). Your task is to generate highly accurate, syntactically valid Manim code in Python that creates a clear, animated explanation of the concept described after the --- separator.
                        The code should:
                        Use the latest Manim Community Edition (manimCE) syntax.
                        Include appropriate scenes, labels, transformations, and animations to effectively visualize and explain the concept.
                        Be structured, readable, and ready to run directly in a manim script.
                        Highlight key ideas, definitions, and transitions to improve understanding.
                        Avoid placeholder code unless absolutely necessary.
                        Output only the code — no commentary or explanation. 
                        --- 
                        {concept}""",
        )
    with open("test.py", "w") as f:
        f.write(response.text)

    return JSONResponse(status_code=200, content=response.text)
