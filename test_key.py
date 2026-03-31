import os
from dotenv import load_dotenv

# Path to the root .env
dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)

key = os.getenv("GROQ_API_KEY")
if not key:
    print("GROQ_API_KEY is NOT set in the environment or .env file.")
else:
    print(f"GROQ_API_KEY is found (Prefix: {key[:5]}...)")
