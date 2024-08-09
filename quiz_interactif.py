import os
from dotenv import load_dotenv
from openai import OpenAI
import random

# Charger les variables d'environnement depuis .env
load_dotenv()

# Initialiser le client OpenAI exactement comme spécifié
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_quiz(num_questions=30):
    questions = []
    prompt = (
        "Générez un QCM en anglais pour un élève de CM2 (5th grade). "
        f"Créez {num_questions} questions adaptées à ce niveau, avec 4 options chacune, "
        "incluant la réponse correcte. Format: Question\\nA. Option\\nB. Option\\nC. Option\\nD. Option\\nRéponse correcte: Lettre"
    )
    
    try:
        response = client.chat.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
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
        
        return questions
    except Exception as e:
        print(f"Erreur lors de la génération du quiz : {e}")
        return []

def administer_quiz(questions):
    score = 0
    random.shuffle(questions)
    
    print("Bienvenue au Quiz d'Anglais pour CM2 (5th Grade) !")
    print("Pour chaque question, entrez la lettre correspondant à votre réponse (A, B, C ou D).")
    
    for i, q in enumerate(questions):
        print(f"\nQuestion {i + 1}: {q['question']}")
        for option in q['options']:
            print(option)
        
        while True:
            user_answer = input("Votre réponse : ").upper()
            if user_answer in ['A', 'B', 'C', 'D']:
                break
            else:
                print("Réponse invalide. Veuillez entrer A, B, C ou D.")
        
        if user_answer == q['correct']:
            score += 1
            print("Correct !")
        else:
            print(f"Incorrect. La bonne réponse était : {q['correct']}")
    
    return score

def main():
    num_questions = 30
    quiz = generate_quiz(num_questions)
    
    if quiz:
        score = administer_quiz(quiz)
        print(f"\nVotre score final : {score}/{num_questions}")
    else:
        print("Impossible de générer le quiz. Veuillez réessayer plus tard.")

if __name__ == "__main__":
    main()

