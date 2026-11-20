from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel
import os
import json

load_dotenv(
    Path(__file__).resolve().parent / ".env",
    override=True #If an environment variable with the same name already exists,override=True allows the value from the .env file to replace it.
)

api_key = os.getenv("NVIDIA_API_KEY")

if not api_key:
    raise ValueError("NVIDIA_API_KEY not found in .env file")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key.strip()
)

Model="nvidia/nemotron-3.5-lightning-30b-a3b"

"---- 1. The problem : unstructured output ----"

# result = client.chat.completions.create(
#     model=Model,
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a helpful assistant"
#         },
#         {
#             "role": "user",
#             "content": "Give me name, age and city of a fictional character"
#         }
#     ]
# )
# print(result.choices[0].message.content)
# print(type(result.choices[0].message.content)) #only give ans in string format

# ---- 2. Naive fix - ask for JSON in the prompt ----

# result = client.chat.completions.create(
#     model=Model,
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a helpful assistant. Response in JSON format"
#         },
#         {
#             "role": "user",
#             "content": "Give me name, age and city of a fictional character"
#         }
#     ]
# )

# print(result.choices[0].message.content)
# print(type(result.choices[0].message.content))


# # Sometimes works, but the model might wrap it in ```json ``` blocks
# # or change the key names, or add extra fields
# # Not reliable enough for production



# ---- What is Pydantic? ----
# Pydantic lets you define the exact "shape" of data you expect.
# Each field has a name and a type (str, int, float, bool, list, etc.)
#
# When you pass text_format=Person, the SDK converts this class into a
# JSON schema and sends it to OpenAI's servers. The model is constrained
# AT THE SERVER LEVEL to only return data that matches this schema.
#
# This is the key difference:
# "Respond in JSON" in the prompt = a suggestion the model can ignore
# text_format=Person = a guarantee enforced before the response reaches you



class Person(BaseModel):
    name: str
    age: int
    city: str


# Create structured output
result = client.chat.completions.create(
    model=Model,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Give me the name, age and city of a fictional person."
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "Person",
            "strict": True,
            "schema": Person.model_json_schema()
        }
    }
)

# Parse the response
person = Person.model_validate_json(
    result.choices[0].message.content
)

print(person)
print(person.name)
print(person.age)
print(person.city)