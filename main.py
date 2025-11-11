from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from dotenv import load_dotenv
import os

load_dotenv()

"""
Decorator - defines a tool 
MANDATORY TO ADD A DOCSTRING BELOW A TOOL FUNCTION to help AI determine when to use th function
"""

@tool
def calculator(a: float, b: float)  -> str:
    """
        A simple tool that performs addition on two floating-point numbers.
        Use this tool for any mathematical addition query.
    """
    print("Tool 1 is working successfully....")
    return f"The sum of {a} and {b} is {a+b}"

@tool
def greeting(name: str)  -> str: # '->' symbol is used to show what is the return type of the function
    """
        A simple tool for greeting the user
    """
    print("Tool 2 is working successfully....")
    return f"Hello {name}, how can I help you today?"

def main():
    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    tools = [calculator, greeting]
    agent_executor = create_agent(model, tools)

    print('Welcome! I am your AI Agent here for your assistance')
    print('Type "exit" to exit')
    print('You can ask me to perform calculations or chat with me.')

    while True:
        user_input = input('\n> ').strip()

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Get complete response
        result = agent_executor.invoke({"messages": [HumanMessage(content=user_input)]})

        print("\nAssistant: ", end="")

        # Extract and print only AI response
        if "messages" in result:    # Checks if the result dictionary contains a "messages" key
            for message in result["messages"]:
                if hasattr(message, 'content') and message.content:
                    if hasattr(message, 'type') and message.type == 'ai':
                        print(message.content)

        """
        if "messages" in result: ---> Checks if the result dictionary contains a "messages" key
            for message in result["messages"]: ---> Loops through all messages in the conversation
                if hasattr(message, 'content') and message.content: ---> checks if the message object has a 'content' attribute and the content is not empty
                    if hasattr(message, 'type') and message.type == 'ai': ---> checks if message has a 'type' attribute and the type is AI response
                        print(message.content) ---> prints the contents of AI responses
                """


if __name__ == "__main__":
    main()
