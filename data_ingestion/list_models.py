import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Ensure API key is set
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not set")

genai.configure(api_key=api_key)

print("Listing available models...")
models = genai.list_models()

print("\nAvailable models:")
for m in models:
    print(f"- {m.name}")
    if hasattr(m, 'supported_generation_methods'):
        print(f"  Supported methods: {m.supported_generation_methods}")
    print()