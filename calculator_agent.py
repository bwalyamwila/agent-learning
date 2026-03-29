import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)

tools = [
    {
      "name": "calculator",
      "description": "A calculator that can perform basic arithmetic operations such as addition, subtraction, multiplication, and division.",
      "input_schema":{
          "type": "object",
          "properties": {
              "operation": {
                  "type" : "string",
                  "enum" : ["add", "subtract", "multiply", "divide"],
                  "description" : "The operation to perform"
              },
              "a" : {
                  "type" : "number",
                  "description" : "First number"
              },
              "b" : {
                  "type" : "number",
                  "description" : "Second number"
              }             
          },
          "required" : ["operation", "a", "b"] 
      }   

    },
    {
        "name" : "weather",
        "description" : "This tool provides the current weather for a given location.",
        "input_schema" : {
            "type" : "object",
            "properties" : {
                "city" : {
                    "type" : "string",
                    "description" : "The city name for which to provide weather information"
                }
            },
            "required" : ["city"]
        }
    }
]

def calculator( operation: str, a: float, b: float) -> float:
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            return "Error: cannot divide by 0"
        return a / b
    else:
        return "Error: Unknown operation"
    

def weather (city: str) -> str:
    weather_data = {
        "new york": "72°F, sunny with light breeze",
        "london": "55°F, rainy",
        "tokyo": "68°F, cloudy",
        "sydney": "77°F, sunny",
        "paris": "60°F, partly cloudy",
        "dubai": "95°F, hot and dry",
    }
    
    city_name = city.lower()
    if city_name in weather_data:
        return weather_data[city_name]
    else:
        return f"Weather data for {city} is not available."




def agent_loop (user_message: str) -> str:

    messages = [
        { "role" : "user", "content": user_message}
    ]

    while True:
        response = client.messages.create(
            model = "claude-opus-4-1-20250805",
            max_tokens = 1024,
            tools = tools,  
            messages = messages
        )

        print(f"\n[Agent thinking...]")
        print(f"Stop reason: {response.stop_reason}")

        if response.stop_reason == "tool_use":
            tool_use_block = None

            for block in response.content:
                if block.type == "tool_use":
                    tool_use_block = block
                    break
            
            if tool_use_block:
                tool_name = tool_use_block.name
                tool_input = tool_use_block.input
                tool_id = tool_use_block.id

                print(f"[Tool called: {tool_name}]")
                print(f"[Input: {tool_input}]")

                if tool_name == "calculator":
                    result = calculator(**tool_input)
                elif tool_name == "weather":
                    result = weather(**tool_input)
                else:
                    result = "Unknown Tool"

                print(f"[Tool result: {result}]")

                messages.append({
                    "role": "assistant",
                    "content": response.content
                })

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": str(result)
                        }
                    ]
                })
        else:
            
            final_response = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_response += block.text
            return final_response

if __name__ == "__main__":
    print("=== Calculator Agent ===\n")
    
    print("Test 1: What is 15 * 7?")
    result = agent_loop("What is 15 * 7?")
    print(f"Agent: {result}\n")
    
    print("Test 2: What is 100 + 50, then divide by 3?")
    result = agent_loop("What is 100 + 50, then divide by 3?")
    print(f"Agent: {result}\n")
    
    print("Test 3: What's 10 divided by 0?")
    result = agent_loop("What's 10 divided by 0?")
    print(f"Agent: {result}\n")

    print("=== Weather Agent ===\n")
    print("Test 4: What's the weather in New York?")
    result = agent_loop("What's the weather in New York?")
    print(f"Agent: {result}\n")

    print("Test 5: What's the weather like in Cape Town?")
    result = agent_loop("What's the weather like in Cape Town?")
    print(f"Agent: {result}\n")




