import json
import re
from datetime import datetime
from openai import OpenAI
from typing import Any,Callable

MODEL='gpt-oss:20b'
BASE_URL = "http://localhost:11434/v1"
MAX_STEPS = 8

def get_current_time() -> str:
    return datetime.now().astimezone().strftime("%I:%M:%S %p %Z")

def calculate(a: float, b: float, operation: str) -> str:
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        result = a / b
    else:
        raise ValueError("Operation must be add, subtract, multiply, or divide.")
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)

def count_words(text: str) -> str:
    if len(text) > 10_000:
        raise ValueError("Text must contain at most 10,000 characters.")
    words = re.findall(r"[^\W_]+(?:[-'][^\W_]+)*", text, flags=re.UNICODE)
    return str(len(words))

TOOLS=[
    {
        'type':'function',
        'function':{
            'name':'get_current_time',
            'description':'Return the current time',
            'parameters':{
                'type':'object',
                'properties':{},
                'required':[]
            }
        }
    },
    {
        'type':'function',
        'function':{
            'name':'calculate',
            'description':'Add, subtract, multiply or divide two numbers.',
            'parameters':{
                'type':'object',
                'properties':{
                    'a':{'type':'number','description':'The first number.'},
                    'b':{'type':'number','description':'The second number.'},
                    'operation':{
                        'type':'string',
                        'enum':['add','subtract','multiply','divide'],
                    },
                },
                'required':['a','b','operation'],
                'additionalProperties':False
            }
        }
    },
    {
        'type':'function',
        'function':{
            'name':'count_words',
            'description':'Count the words in a piece of text.',
            'parameters':{
                'type':'object',
                'properties':{
                    'text':{'type':'string','description':'The exact text whose words should be counted.'},
                },
                'required':['text'],
                'additionalProperties':False
            },
        },
    },
]

TOOL_DISPATCH: dict[str,Callable[...,str]]={
    'get_current_time':get_current_time,
    'calculate':calculate,
    'count_words':count_words
}


def run_tool(name:str,arguments:dict[str,Any])->str:
    function=TOOL_DISPATCH.get(name)
    if function is None:
        raise ValueError(f'Unknown tool {name}')
    return str(function(**arguments))
  
def run_agent(user_message:str,client:OpenAI)->str:
    messages:list[Any]=[
        {
            'role':'system',
            'content':(
                "Use the available tools whenever they are needed. "
                "Never invent a tool result."
            ),
        },
        {
            'role':'user',
            'content':user_message
        }
    ]
    for _step in range(1, MAX_STEPS + 1):
            response=client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS
                )
        
    
            message=response.choices[0].message
            messages.append(message.model_dump(exclude_none=True))
    
            if not message.tool_calls:
                return message.content or "The model returned no text."
    
            for tool_call in message.tool_calls:
                arguments=json.loads(tool_call.function.arguments or '{}')

                result=run_tool(
                    tool_call.function.name,
                    arguments
                )
           
                messages.append({
                'role':'tool',
                'tool_call_id':tool_call.id,
                'content':result
                })

    return f"Stopped after {MAX_STEPS} model turns without a final answer."

def main()->None:
    client=OpenAI(
    base_url=BASE_URL,
    api_key='ollama'
    )

    prompt=input('You: ').strip()
    if prompt:
        print(f'\nAgent: {run_agent(prompt,client)}')

if __name__=='__main__':
    main()



