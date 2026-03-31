"""Test the ACTUAL listed embedding models"""
from google import genai
from google.genai import types
import json

API_KEY = "AIzaSyAjWq08tjh3VuOLOAm3AeynVLaBuVUium8"
results = {}

for api_ver in ["v1alpha", "v1beta", "v1"]:
    client = genai.Client(api_key=API_KEY, http_options=types.HttpOptions(api_version=api_ver))
    for model in ["gemini-embedding-001", "gemini-embedding-2-preview"]:
        key = f"{api_ver}_{model}"
        try:
            response = client.models.embed_content(model=model, contents="hello world")
            results[key] = f"Success: dim={len(response.embeddings[0].values)}"
        except Exception as e:
            results[key] = f"Fail: {str(e)[:150]}"

with open("api_results.json", "w") as f:
    json.dump(results, f, indent=2)
