import openai
import random
import time
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress
from config import API_KEY  # Importer la clé API depuis config.py

# Configurer l'API d'OpenAI
openai.api_key = API_KEY

console = Console()

# Catégories de questions
CATEGORIES = ["Reading Comprehension", "Vocabulary", "Grammar", "Literary Analysis"]

def generate_question(category):
    """
    Génère une question à choix multiples pour la catégorie donnée.

    Args:
        category (str): La catégorie de la question à générer.

    Returns:
        str: La question générée ou un message d'erreur.
    """
    prompt = (
        f"Generate a multiple choice question in English suitable for a 6th grade student. "
        f"The question should cover {category}. "
        "Provide four answer choices and indicate the correct answer."
    )
    try:
        response = openai.Completion.create(
            engine="text-davinci-004",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        question = response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        console.print(f"[red]Error generating question: {e}[/red]")
        question = f"Error: Could not generate {category} question. Using a default question instead."
        question += "\nWhat is the capital of France?\nA. Paris\nB. London\nC. Berlin\nD. Madrid"
    return question

def create_qcm(num_questions=25):
    """
    Crée un ensemble de questions à choix multiples.

    Args:
        num_questions (int): Le nombre de questions à générer.

    Returns:
        list: Une liste de tuples (catégorie, question).
    """
    questions = []
    for _ in range(num_questions):
        category = random.choice(CATEGORIES)
        question = generate_question(category)
        questions.append((category, question))
    return questions

def extract_correct_answer(question):
    """
    Extrait la réponse correcte d'une question.

    Args:
        question (str): La question complète avec les choix.

    Returns:
        str: La lettre de la réponse correcte.
    """
    choices = question.split('\n')
    correct_answer = choices[1]  # Suppose that the first choice is the correct answer
    return correct_answer.split(' ')[0]  # Extract the letter of the correct answer (A, B, C, or D)

def show_hint(question):
    """
    Affiche un indice pour la question donnée.

    Args:
        question (str): La question complète avec les choix.
    """
    choices = question.split('\n')[1:]  # Get all choices
    correct_answer = extract_correct_answer(question)
    wrong_answers = [choice for choice in choices if choice[0] != correct_answer]
    eliminated = random.choice(wrong_answers)
    console.print(f"[italic yellow]Hint: The answer is probably not {eliminated}[/italic yellow]")

def main():
    """
    Fonction principale qui gère le déroulement du jeu.
    """
    console.print("[bold blue]Welcome to the English Multiple Choice Quiz for 6th Grade Students![/bold blue]")
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
            else:
                console.print(f"[red]Incorrect. The correct answer was {correct_answer}.[/red]")

        play_again = Prompt.ask("Do you want to play again? (yes/no)")
        if play_again.lower() != 'yes':
            break

if __name__ == "__main__":
    main()

