from flask import Flask, request, jsonify, Response
import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

BASE_URL = "https://generativelanguage.googleapis.com"
INPUT_API_KEY = "GOOGLE_API_KEY_"
OUTPUT_API_KEY = "OUTPUT_API_KEY"
PORT = "PORT"

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

@app.route("/", methods=["GET"])
def index():
    output_api_key = os.getenv(OUTPUT_API_KEY)
    if output_api_key:
        return f"Google AI API Proxy is Running.", 200
    else:
        return "not found output_api_key", 200
    
@app.route("/<path:path>", methods=["GET", "POST", "OPTIONS"])
def proxy(path):
    """Handle proxy requests to Google AI API."""
    if request.method == "OPTIONS":
        return Response(
            status=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Authorization, x-api-key, x-goog-api-key, Content-Type"
            }
        )

    api_key = get_api_key()
    if not api_key:
        return jsonify({"error": "no chossing_key"}), 401

    target_url = f"{BASE_URL}/{path}"
    if request.query_string:
        target_url += f"?{request.query_string.decode('utf-8')}"

    headers = {
        "X-Goog-Api-Key": api_key,
        "Content-Type": request.headers.get("Content-Type", "")
    }

    try:
        if request.method == "POST":
            response = requests.post(target_url, headers=headers, data=request.data)
        else:
            response = requests.get(target_url, headers=headers)

        response_headers = {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": response.headers.get("Content-Type", "")
        }

        if "application/json" in response.headers.get("Content-Type", ""):
            return Response(response.content, status=response.status_code, headers=response_headers)
        elif "text/event-stream" in response.headers.get("Content-Type", ""):
            return Response(response.iter_content(chunk_size=1024), status=response.status_code, headers=response_headers)
        else:
            return Response(response.content, status=response.status_code, headers=response_headers)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with more details."""
    message = str(error)  
    return jsonify({"error": "Not Found", "message": message}), 404

if __name__ == "__main__":
    port = int(os.getenv(PORT, 8000))
    app.run(host="0.0.0.0", port=port, debug=True)