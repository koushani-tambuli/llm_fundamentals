from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os
import json

# Load environment variables
load_dotenv(
    Path(__file__).resolve().parent / ".env",
    override=True
)

# Create NVIDIA client
api_key = os.getenv("NVIDIA_API_KEY")

if not api_key:
    raise ValueError("NVIDIA_API_KEY not found in .env file")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key.strip()
)

models = client.models.list()

for model in models.data:
    print(model.id)