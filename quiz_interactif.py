import os
from dotenv import load_dotenv
from openai import OpenAI
import random
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

def generate_quiz(num_questions=30):
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

def administer_quiz(questions):
    score = 0
    random.shuffle(questions)
    
    logging.info("Bienvenue au Quiz d'Anglais pour CM2 (5th Grade) !")
    logging.info("Pour chaque question, entrez la lettre correspondant à votre réponse (A, B, C ou D).")
    
    for i, q in enumerate(questions):
        logging.info(f"\nQuestion {i + 1}: {q['question']}")
        for option in q['options']:
            logging.info(option)
        
        while True:
            user_answer = input("Votre réponse : ").upper()
            if user_answer in ['A', 'B', 'C', 'D']:
                break
            else:
                logging.info("Réponse invalide. Veuillez entrer A, B, C ou D.")
        
        if user_answer == q['correct']:
            score += 1
            logging.info("Correct !")
        else:
            logging.info(f"Incorrect. La bonne réponse était : {q['correct']}")
    
    return score

def main():
    num_questions = 5  # Réduit pour le test en CI/CD
    logging.info("Début de l'exécution du script")
    quiz = generate_quiz(num_questions)
    
    if quiz:
        if 'CI' in os.environ:  # Vérifie si on est dans un environnement CI
            logging.info(f"Quiz généré avec succès. {len(quiz)} questions créées.")
            for q in quiz:
                logging.info(f"Question: {q['question']}")
                logging.info(f"Réponse correcte: {q['correct']}")
        else:
            score = administer_quiz(quiz)
            logging.info(f"\nVotre score final : {score}/{num_questions}")
    else:
        logging.error("Impossible de générer le quiz.")
    
    logging.info("Fin de l'exécution du script")

if __name__ == "__main__":
    main()