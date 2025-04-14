from flask import Flask, request, jsonify, Response
import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

BASE_URL = "https://generativelanguage.googleapis.com"
INPUT_API_KEY = "GOOGLE_API_KEY_"

def get_api_key():
    api_keys = [
        os.getenv(key)
        for key in os.environ
        if key.startswith(INPUT_API_KEY) and os.getenv(key)
    ]
    if not api_keys:
        print("Error: No API keys found in environment variables.")
        return None 
    return random.choice(api_keys)
    
@app.route("/<path:path>", methods=["GET", "POST", "OPTIONS"])
def proxy(path):
    api_key = get_api_key()
    if not api_key:
        return jsonify({"error": "no api_key"}), 401
    
    target_url = f"{BASE_URL}/{path}"
    headers = {
        "X-Goog-Api-Key": api_key,
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*" 
    }
    data = request.get_json()
    data['safetySettings'] = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "OFF"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "OFF"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "OFF"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "OFF"
        },
        {
            "category": "HARM_CATEGORY_CIVIC_INTEGRITY",
            "threshold": "OFF"
        }
    ]
    response = requests.post(target_url, headers=headers, json=data)
    return Response(response.content, status=response.status_code, headers={"Content-Type": "application/json"})                                                                            
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
