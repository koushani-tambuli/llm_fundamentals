# LLM Fundamentals 🚀

A beginner-friendly learning repository where I explore the fundamentals of **Large Language Models (LLMs)** using Python and the NVIDIA NIM API.

This repository contains my practice code, experiments, and notes as I learn how to interact with LLMs and understand their capabilities.

I'm still learning, so this repository will continue to grow as I explore more concepts.

## 📚 Topics Covered

- **LLM API Integration:** Connecting to LLMs using the OpenAI Python SDK and NVIDIA NIM API.
- **Chat Completions:** Sending prompts and receiving responses from an LLM.
- **Multi-turn Conversations:** Understanding how message history is used in conversations.
- **Model Parameters:** Experimenting with temperature, max tokens, and system prompts.
- **Structured Outputs:** Generating structured responses using Pydantic.
- **JSON Responses:** Understanding the difference between normal text responses and structured JSON.
- **Tool Calling (Function Calling):** Learning how an LLM can interact with external Python functions.
- **Environment Variables:** Managing API keys securely using `.env` files.

## 🛠️ Tech Stack

- Python
- NVIDIA NIM API
- OpenAI Python SDK
- Pydantic
- python-dotenv
- Requests

## 📂 Repository Structure

```text
llm_fundamentals/
│
├── .env.example
├── .gitignore
│
├── llm.py
├── structed_output.py
├── tools_calls.py
│
├── llm.txt
├── tool_calls.txt
│
├── test.py
│
└── README.md
```

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/koushani-tambuli/llm_fundamentals.git
```

### 2. Navigate to the project directory

```bash
cd llm_fundamentals
```

### 3. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install openai python-dotenv pydantic requests
```

### 5. Configure your API key

Create a `.env` file in the root directory.

Copy the contents of `.env.example` into it and add your NVIDIA API key:

```env
NVIDIA_API_KEY=your_api_key_here
```

You can get an API key from [NVIDIA NIM](https://build.nvidia.com/).

**Note:** Never upload your actual `.env` file or API key to GitHub.

## ▶️ Running the Examples

Run the Python files individually:

```bash
python llm.py
```

```bash
python structed_output.py
```

```bash
python tools_calls.py
```

Each file explores a different LLM concept.

## 🎯 Purpose of This Repository

The goal of this repository is to build a practical understanding of LLM development, starting with the basics and gradually moving towards more advanced concepts.

This is a learning project, not a production-ready application.

I will keep adding experiments and improving my understanding as I learn.

## 🌱 Learning in Progress

More concepts and experiments will be added as I continue exploring the world of LLMs.

---

**Made while learning, experimenting, and building with LLMs.** 💻
