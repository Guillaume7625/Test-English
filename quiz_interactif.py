try:
    from rich.console import Console
except ImportError:
    print("Rich library not found. Please install it using 'pip install rich'")
    exit(1)
import os
import random
import time
import openai
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress

# Charger les variables d'environnement
load_dotenv()

# Configurer la clé API OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialiser la console Rich
console = Console()

# Catégories de questions
CATEGORIES = ["Reading Comprehension", "Vocabulary", "Grammar", "Literary Analysis"]

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.level = 1
        self.experience = 0

    def add_score(self, points):
        self.score += points
        self.experience += points
        if self.experience >= self.level * 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        console.print(f"[bold yellow]Congratulations! You've reached level {self.level}![/bold yellow]")

def generate_question(category):
    prompt = (
        f"Generate a multiple choice question in English suitable for a 6th grade student. "
        f"The question should cover {category}. "
        "Provide four answer choices and indicate the correct answer."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        question = response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        console.print(f"[red]Error generating question: {e}[/red]")
        question = f"Error: Could not generate {category} question. Using a default question instead."
        question += "\nWhat is the capital of France?\nA. Paris\nB. London\nC. Berlin\nD. Madrid"
    return question

def create_qcm(num_questions=25):
    questions = []
    for _ in range(num_questions):
        category = random.choice(CATEGORIES)
        question = generate_question(category)
        questions.append((category, question))
    return questions

def extract_correct_answer(question):
    choices = question.split('\n')
    correct_answer = choices[1]
    return correct_answer.split(' ')[0]

def show_hint(question):
    choices = question.split('\n')[1:]
    correct_answer = extract_correct_answer(question)
    wrong_answers = [choice for choice in choices if choice[0] != correct_answer]
    eliminated = random.choice(wrong_answers)
    console.print(f"[italic yellow]Hint: The answer is probably not {eliminated}[/italic yellow]")

def main():
    console.print("[bold blue]Welcome to the English Multiple Choice Quiz for 6th Grade Students![/bold blue]")
    player_name = Prompt.ask("Enter your name")
    player = Player(player_name)

    while True:
        questions = create_qcm()
        
        for i, (category, question) in enumerate(questions, 1):
            console.print(f"[bold]Question {i} - Category: {category}[/bold]")
            console.print(question)

            with Progress() as progress:
                task = progress.add_task("[green]Time remaining...", total=30)
                response = None
                start_time = time.time()

                while not progress.finished:
                    if response:
                        break
                    response = Prompt.ask("Your answer (A, B, C, or D), or 'H' for a hint", default="")
                    if response.upper() == 'H':
                        show_hint(question)
                        response = None
                    progress.update(task, completed=30 - (time.time() - start_time))

            if not response:
                console.print("[red]Time's up! Moving to the next question.[/red]")
                continue

            correct_answer = extract_correct_answer(question)
            if response.strip().lower() == correct_answer.strip().lower():
                console.print("[green]Correct! Well done![/green]")
                points = max(1, int(30 - (time.time() - start_time)))
                player.add_score(points)
                console.print(f"[green]You earned {points} points![/green]")
            else:
                console.print(f"[red]Incorrect. The correct answer was {correct_answer}.[/red]")

        console.print(f"[bold]Your final score is {player.score}.[/bold]")
        console.print(f"[bold]Your current level is {player.level}.[/bold]")
        
        if player.score >= 100:
            console.print("[gold1]Fantastic job! You're a language master![/gold1]")
        elif player.score >= 75:
            console.print("[yellow]Great work! You're on your way to becoming a language expert![/yellow]")
        elif player.score >= 50:
            console.print("[orange3]Good effort! Keep practicing to improve your skills![/orange3]")
        else:
            console.print("[red]Keep studying! Every question is an opportunity to learn![/red]")

        play_again = Prompt.ask("Do you want to play again? (yes/no)")
        if play_again.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
