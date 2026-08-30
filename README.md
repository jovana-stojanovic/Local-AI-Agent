# Local AI Tool-Calling Agent

A simple local AI agent built with Python, Ollama, and an OpenAI-compatible API.

The agent can understand a user's request, decide when a tool is needed, execute the appropriate Python function, and use the tool result to generate a final response.

## Features

* Local LLM inference using Ollama
* OpenAI-compatible API
* Function/tool calling
* Multiple custom tools
* Multi-step agent loop
* JSON argument handling
* Tool dispatch system
* Maximum step limit to prevent infinite execution

## Available Tools

### `get_current_time`

Returns the current local date and time of the computer.

### `calculate`

Performs basic arithmetic operations:

* Addition
* Subtraction
* Multiplication
* Division

### `count_words`

Counts the words in a given piece of text.

## How It Works

The agent follows this basic loop:

```text
User
  ↓
LLM
  ↓
Tool call
  ↓
Python function
  ↓
Tool result
  ↓
LLM
  ↓
Final answer
```

The model decides which tool to use based on the user's request. Python then executes the selected function and sends the result back to the model.

## Example

### User

```text
Tell me the current time, multiply 18 by 7, and count the words in
"Agents connect models to useful actions."
```

### Agent

```text
- Current time: 01:59:12 PM
- 18 × 7 = 126
- Word count: 6
```

## Project Structure

```text
ai-agent/
│
├── agent.py
├── README.md
└── ...
```

## Requirements

* Python 3.14+
* Ollama
* `gpt-oss:20b`
* OpenAI Python package

## Setup

Install the OpenAI Python package:

```bash
pip install openai
```

Make sure Ollama is installed and the model is available locally:

```bash
ollama pull gpt-oss:20b
```

The application uses the following local OpenAI-compatible endpoint:

```text
http://localhost:11434/v1
```

## Run

Start the agent with:

```bash
python agent.py
```

Then enter a request when prompted:

```text
You: What is 25 multiplied by 4?
```

The model can decide to call the `calculate` tool and return the result.

## Technologies

* Python
* Ollama
* gpt-oss:20b
* OpenAI Python SDK
* JSON
* Regular Expressions
* Function Calling
