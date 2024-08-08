try:
    from rich.console import Console
except ImportError:
    print("Rich library not found. Please install it using 'pip install rich'")
    exit(1)
try:
    from rich.console import Console
except ImportError:
    print("Rich library not found. Please install it using 'pip install rich'")
    exit(1)
try:
    from rich.console import Console
except ImportError:
    print("Rich library not found. Please install it using 'pip install rich'")
    exit(1)
try:
    from rich.console import Console
except ImportError:
    print("Rich library not found. Please install it using 'pip install rich'")
    exit(1)
try:
    from rich.console import Console
except ImportError:
    print("Rich library not found. Please install it using 'pip install rich'")
    exit(1)
import sys
from rich.console import Console
from rich.prompt import Prompt

# ... (le reste du code existant)

def main(test_mode=False):
    console = Console()
    console.print("Welcome to the English Multiple Choice Quiz for 6th Grade Students!")
    
    if test_mode:
        player_name = "Test User"
    else:
        player_name = Prompt.ask("Enter your name")
    
    # ... (le reste du code existant)

if __name__ == "__main__":
    test_mode = "--test" in sys.argv
    main(test_mode)
