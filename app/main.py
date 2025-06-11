from fastapi import Request, FastAPI
import os
from fastapi.responses import JSONResponse
from google import genai
from mistralai import Mistral
from dotenv import load_dotenv
import json
import re
from app.services.model_service import generateUsingMistral, generateUsingGemini

load_dotenv()

API_KEY= os.environ.get("AI_API_KEY")
MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]


if not API_KEY or not MISTRAL_API_KEY:
    raise RuntimeError("AI_API_KEY is not set in the environment or .env file")


app = FastAPI()
client = genai.Client(api_key=API_KEY)
mistral_client = Mistral(api_key=MISTRAL_API_KEY)

mistral_model = "codestral-latest"



@app.get("/")
def root():
    return {"message from server":"Hello World!"}

@app.post("/generate-manim")
async def generateManim(request: Request):

    payload = await request.json()
    concept = payload.get("concept")
    model = payload.get("model")

    if model == "gemini":
        generated_content = generateUsingGemini(concept)
    else:
        generated_content = generateUsingMistral(concept)

    cleaned_content = re.sub(r'^```json\s*', '', generated_content.strip())
    cleaned_content = re.sub(r'\s*```$', '', cleaned_content)
    json_data = json.loads(cleaned_content)

    fileName = hash(concept)
    
    with open(f"./generations/{fileName}.py", "w") as f:
        f.write(json_data["manim"])
    with open(f"./generations/{fileName}-script.txt", "w") as f:
        f.write(json_data["script"])

    return JSONResponse(status_code=200, content=json_data["script"])
