
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

MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"


# ---- 1. Simplest API call ----
result = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": "What is the square root of 49?"}
    ]
)


# ---- 2. Full response ----
#print(result)


# ---- 2.5. Raw JSON response ----
print(json.dumps(result.model_dump(), indent=2, default=str))


# ---- 3. Extract text ----
print(result.choices[0].message.content)

print(result.choices[0].message.reasoning_content)
 


# ---- 4. Multi-turn conversation ----
# messages = [
#     {"role": "user", "content": "My name is Harish"}
# ]

# messages.append({
#     "role": "assistant",
#     "content": "Nice to meet you, Harish!"
# })

# messages.append({
#     "role": "user",
#     "content": "What is my name?"
# })

# response = client.chat.completions.create(
#     model=MODEL,
#     messages=messages
# )

# print(response.choices[0].message.content)


# ---- 5. System prompt, temperature, max tokens ----

# result = client.chat.completions.create(
#     model=MODEL,
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a helpful assistant who makes jokes."
#         },
#         {
#             "role": "user",
#             "content": "What is the square root of 49?"
#         }
#     ],
#     temperature=0.7,
#     max_tokens=256,
#     extra_body={
#         "chat_template_kwargs": {
#             "enable_thinking": False
#         }
#     }
# )

# print(result.choices[0].message.content)



# # ---- 6. Token usage ----
# print("Input tokens:", result.usage.prompt_tokens)
# print("Output tokens:", result.usage.completion_tokens)
# print("Total tokens:", result.usage.total_tokens)


# ---- 7. Streaming ----
# stream = client.chat.completions.create(
#     model=MODEL,
#     messages=[
#         {
#             "role": "user",
#             "content": "Tell me a short story about a robot."
#         }
#     ],
#     stream=True
# )

# for chunk in stream:
#     content = chunk.choices[0].delta.content
#     if content:
#         print(content,end="", flush=True)
