import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import logging

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Chargement des variables d'environnement
load_dotenv()
logging.info("Variables d'environnement chargées")

# Initialisation du client OpenAI
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    logging.error("La clé API OpenAI n'est pas définie dans les variables d'environnement ou le fichier .env")
    raise ValueError("Clé API OpenAI manquante")
logging.info("Clé API OpenAI trouvée")
client = OpenAI(api_key=api_key)
logging.info("Client OpenAI initialisé")

def generate_quiz(num_questions=10):
    logging.info(f"Génération d'un quiz avec {num_questions} questions")
    questions = []
    prompt = (
        "Générez un QCM en anglais pour un élève de CM2 (5th grade). "
        f"Créez {num_questions} questions adaptées à ce niveau, avec 4 options chacune, "
        "incluant la réponse correcte. Format: Question\\nA. Option\\nB. Option\\nC. Option\\nD. Option\\nRéponse correcte: Lettre"
    )
    
    try:
        logging.info("Envoi de la requête à l'API OpenAI")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        logging.info("Réponse reçue de l'API OpenAI")
        raw_quiz = response.choices[0].message.content.strip()
        
        for question in raw_quiz.split('\n\n'):
            if question:
                parts = question.split('\n')
                question_text = parts[0].strip()
                options = parts[1:5]
                correct_answer = parts[5].split(': ')[1]
                
                questions.append({
                    "question": question_text,
                    "options": options,
                    "correct": correct_answer
                })
        
        logging.info(f"{len(questions)} questions générées avec succès")
        return questions
    except Exception as e:
        logging.error(f"Erreur lors de la génération du quiz : {e}")
        return []

def update_html_with_quiz(questions):
    with open('index.html', 'r') as file:
        html_content = file.read()
    
    quiz_data = json.dumps(questions)
    updated_html = html_content.replace('let quizData = [];', f'let quizData = {quiz_data};')
    
    with open('index.html', 'w') as file:
        file.write(updated_html)
    
    logging.info("Fichier HTML mis à jour avec les nouvelles questions")

if __name__ == "__main__":
    quiz = generate_quiz()
    update_html_with_quiz(quiz)
