import os
import openai
try:
    from rich.console import Console
except ImportError:
    print("Rich library not found. Please install it using 'pip install rich'")
    exit(1)

openai.api_key = os.getenv('OPENAI_API_KEY')

def main_function():
    return "Hello, World!"

if __name__ == "__main__":
    console = Console()
    console.print(main_function())
