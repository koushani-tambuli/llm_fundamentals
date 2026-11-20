
from openai import OpenAI, APIStatusError
from dotenv import load_dotenv
from pathlib import Path
import os
import json
import requests

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

def get_weather(city: str):
    

    # STEP 1: Convert city name into geographical coordinates
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    geo_response = requests.get(geo_url, params=geo_params, timeout=15)
    geo_response.raise_for_status()

    geo_data = geo_response.json()

    if not geo_data.get("results"):
        return {"error": f"City '{city}' not found"}

    location = geo_data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]
    city_name = location["name"]

    # STEP 2: Fetch current weather using coordinates
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "weather_code",
            "wind_speed_10m"
        ],
        "timezone": "auto"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params,
        timeout=15
    )

    weather_response.raise_for_status()

    weather_data = weather_response.json()
    current = weather_data["current"]

    # STEP 3: Convert weather code into readable description
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm"
    }

    condition = weather_codes.get(
        current["weather_code"],
        "Unknown weather condition"
    )

    # STEP 4: Return actual weather information
    return {
        "city": city_name,
        "temperature": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "unit": "celsius",
        "condition": condition,
        "last_updated": current["time"]
    }


# ---- 1. Define the actual Python function ----
# def get_weather(city: str):
#     return {
#         "city": city,
#         "temperature": 28,
#         "unit": "celsius",
#         "condition": "sunny"
#     }
#This is just an example function

# ---- 2. Describe the function to the model ----
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city to get weather for"
                    }
                },
                "required": ["city"]
            }
        }
    }
]


# ---- 3. Send the question and tools to NVIDIA ----
messages = [
    {
        "role": "user",
        "content": "What is the current weather in Delhi?"
    }
]

result = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools,
    tool_choice="auto",
    temperature=0.2,
    max_tokens=1024
)


# ---- 4. Extract the model's response ----
assistant_message = result.choices[0].message

# Check whether the model requested a function call
if assistant_message.tool_calls:

    # Add the assistant's tool-call message to history
    messages.append(
        assistant_message.model_dump(exclude_none=True)
    )

    # ---- 5. Execute the requested function ----
    for tool_call in assistant_message.tool_calls:

        function_name = tool_call.function.name
        function_args = json.loads(
            tool_call.function.arguments
        )

        if function_name == "get_weather":
            function_result = get_weather(
                function_args["city"]
            )
        else:
            raise ValueError(f"Unknown function: {function_name}")

        print(f"🔧 Tool called: {function_name}")
        print(f"📦 Raw result: {function_result}")

        # ---- 6. Send the function result back to NVIDIA ----
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(function_result)
        })

    # ---- 7. Ask NVIDIA to generate the final answer ----
    final_result = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=1024
    )

    print("\n💬 Final answer:")
    print(final_result.choices[0].message.content)

else:
    # Model answered without requesting a function
    print(assistant_message.content)