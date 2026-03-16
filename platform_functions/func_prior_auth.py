import json
import requests

GEMINI_API_KEY = "AIzaSyBNWtSErzZGz7o9M9Tggj0LW_uG3uAAfyc"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def classify_json(data: dict) -> dict:
    prompt = f"""Classify this healthcare JSON as 'prior_auth' or 'claim'.
Reply ONLY with JSON: {{"classification": "prior_auth|claim|unknown", "confidence": "high|medium|low", "reasoning": "one sentence"}}

{json.dumps(data)}"""

    r = requests.post(URL, json={
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0, "responseMimeType": "application/json"}
    }, timeout=30)

    r.raise_for_status()
    return json.loads(r.json()["candidates"][0]["content"]["parts"][0]["text"])


if __name__ == "__main__":
    try:
        raw = input("Input JSON:")
        result = classify_json(json.loads(raw))
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError:
        print("Invalid JSON. Please paste valid JSON.")