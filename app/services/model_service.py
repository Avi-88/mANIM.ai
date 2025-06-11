from google import genai
from mistralai import Mistral
import os
from dotenv import load_dotenv
import re
import json

load_dotenv()

GEMINI_API_KEY= os.environ.get("AI_API_KEY")
MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]


if not GEMINI_API_KEY or not MISTRAL_API_KEY:
    raise RuntimeError("API key for one or more models is not set in the environment or .env file")


gemini_client = genai.Client(api_key=GEMINI_API_KEY)
mistral_client = Mistral(api_key=MISTRAL_API_KEY)

mistral_model = "codestral-latest"
gemini_model = "gemini-2.0-flash"


def generateUsingGemini(concept):
    try:
        generated_content =  gemini_client.models.generate_content(
            model=gemini_model,
            contents=f"""
                        Concept = {concept}

                        You are an expert in Manim (Mathematical Animation Engine). Your task is to generate a JSON object with two fields:

                        1. `"manim"`: Fully valid Python code that uses Manim to create a clear animation explaining the concept described before these instructions.
                        2. `"script"`: A narration script aligned with the animation. Each line should describe what the viewer is seeing at that moment. This will be used to generate audio, so timing must closely match the animation's pacing and duration.

                        Strict Instructions for `"manim"`:
                        - Start with `from manim import *`
                        - Define a class named `Animation` inheriting from a Scene subclass (e.g., `Scene`, `MovingCameraScene`, etc.)
                        - Implement a `construct(self)` method with complete animation logic.
                        - Use only Manim primitives and official documentation: https://docs.manim.community
                        - Do NOT include or reference any external media (images, SVGs, fonts, audio).
                        - Do NOT use `.rotate()` on NumPy arrays like `UP`, `DOWN`, or `get_center()`; use `rotate_vector(vec, angle)` instead.
                        - Do NOT create overlapping text or objects and make sure they stay within the video frame.
                        - The code must be syntactically correct and runnable as-is.
                        - Make sure the video length matches with the script length, maintain the pace accordingly
                        - No markdown, comments, or explanations — just raw Python code in the `"manim"` field.

                        Strict Instructions for `"script"`:
                        - Provide a sequence of narration lines.
                        - Make sure that the lines  match with the video, based on how long the corresponding animation takes.
                        - DO NOT include
                        - Describe clearly the concept which matches what's happening visually.
                        - Avoid filler; keep narration tight, informative, and in sync with the visuals.

                        Return the output strictly in **JSON format** as shown below:
                        ```json
                        {{
                        "manim": "<valid Python Manim code>",
                        "scrip": "Sunlight has essential elements that plants use to generate their food..."
                        }}
                        """,
        ).text

        return generated_content
    except json.JSONDecodeError as e:
        print("JSON parsing failed:", e)
        print("Raw response:", generated_content)
        raise

    except Exception as e:
        print("Unexpected error:", e)
        raise


def generateUsingMistral(concept):
    try:
        message = [{"role": "user", "content": f"""
                            Concept = {concept}

                            You are an expert in Manim (Mathematical Animation Engine). Your task is to generate a JSON object with two fields:

                            1. `"manim"`: Fully valid Python code that uses Manim to create a clear animation explaining the concept described before these instructions in great detail.
                            2. `"script"`: A narration script aligned with the animation. Each line should describe what the viewer is seeing at that moment. This will be used to generate audio, so timing must closely match the animation's pacing and duration.

                            Strict Instructions for `"manim"`:
                            - Start with `from manim import *`
                            - Define a class named `Animation` inheriting from a Scene subclass (e.g., `Scene`, `MovingCameraScene`, etc.)
                            - Implement a `construct(self)` method with complete animation logic.
                            - Use only Manim primitives and official documentation: https://docs.manim.community
                            - DO NOT include or reference any external media (images, SVGs, fonts, audio).
                            - DO NOT use `.rotate()` on NumPy arrays like `UP`, `DOWN`, or `get_center()`; use `rotate_vector(vec, angle)` instead.
                            - DO NOT EVER create overlapping text or objects and make sure they stay within the video frame.
                            - The code must be syntactically correct and runnable as-is.
                            - Make sure the video length matches with the script length, maintain the pace accordingly
                            - No markdown, comments, or explanations — just raw Python code in the `"manim"` field.

                            Strict Instructions for `"script"`:
                            - Provide a sequence of narration lines.
                            - Make sure that the lines  match with the video, based on how long the corresponding animation takes.
                            - Describe clearly the concept which matches what's happening visually.
                            - Avoid filler; keep narration tight, informative, and in sync with the visuals.

                            Return the output strictly in **JSON format** as shown below:
                            ```json
                            {{
                            "manim": "<valid Python Manim code>",
                            "scrip": "Sunlight has essential elements that plants use to generate their food..."
                            }}
                            """}]
        
        chat_response = mistral_client.chat.complete(
            model = mistral_model,
            messages = message
        )   
        generated_content = chat_response.choices[0].message.content

        return generated_content
    except json.JSONDecodeError as e:
        print("JSON parsing failed:", e)
        print("Raw response:", generated_content)
        raise

    except Exception as e:
        print("Unexpected error:", e)
        raise


        

    