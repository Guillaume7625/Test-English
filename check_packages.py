import sys
import subprocess

packages = ["openai", "python-dotenv", "rich"]

for package in packages:
    try:
        __import__(package)
        print(f"{package} is installed.")
    except ImportError as e:
        print(f"{package} is not installed. Error: {e}")

print("\nListe des packages installés :")
result = subprocess.run([sys.executable, '-m', 'pip', 'list'], capture_output=True, text=True)
print(result.stdout)

