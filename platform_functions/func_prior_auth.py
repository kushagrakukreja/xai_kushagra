import json
import requests

GEMINI_API_KEY = "AIzaSyBf_1aXOZjgf1fcEIDXy4_LewYrV5R75pg"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def func_prior_auth(config, **input_obj) -> dict:
    prompt = f"""Classify this healthcare JSON as 'prior_auth' or 'claim'.
Reply ONLY with JSON: {{"classification": "prior_auth|claim|unknown", "confidence": "high|medium|low", "reasoning": "one sentence"}}

{json.dumps(input_obj)}"""

    r = requests.post(URL, json={
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0, "responseMimeType": "application/json"}
    }, timeout=30)

    r.raise_for_status()
    return json.loads(r.json()["candidates"][0]["content"]["parts"][0]["text"])