import json
import requests

PRIOR_AUTH_API = "https://mq-proxy.twenty512.atlantis.xpms.ai/pipeline/dag/execute/workflow_355b9528-d463-48f9-8cc9-76cfe545b03a"
CLAIMS_API = "https://mq-proxy.twenty512.atlantis.xpms.ai/pipeline/dag/execute/workflow_44f760e9-cabf-47e0-818a-820a2e15f83a"

api_key = "AIzaSyBz7n2qG0DmSVspqQXpRrAScYO4z1hhVKc"
gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"



def func_prior_auth(config, **input_obj) -> dict:
    
    # Step 1: Classify the input JSON
    prompt = f"""Classify this healthcare JSON as 'prior_auth' or 'claim'.
Reply ONLY with JSON: {{"classification": "prior_auth|claim|unknown", "confidence": "high|medium|low", "reasoning": "one sentence"}}

{json.dumps(input_obj)}"""

    r = requests.post(gemini_url, json={
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0, "responseMimeType": "application/json"}
    }, timeout=30)
    r.raise_for_status()

    classification = json.loads(r.json()["candidates"][0]["content"]["parts"][0]["text"])

    # Step 2: Route to the correct API based on classification
    target = classification.get("classification")

    if target == "prior_auth":
        api_url = PRIOR_AUTH_API
    elif target == "claim":
        api_url = CLAIMS_API
    else:
        return {**classification, "routed_to": None, "api_response": "Skipped — classification was unknown"}

    api_response = requests.post(api_url, json=input_obj, timeout=30)
    api_response.raise_for_status()

    return {
        **classification,
        "routed_to": target,
        "api_response": api_response.json()
    }