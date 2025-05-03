from flask import Blueprint, jsonify, request
import random

switch_question_bp = Blueprint('switch_question', __name__)

# Mock data 15 questions
QUESTIONS = [
    {"id": 1, "difficulty": "easy", "question": "What is 2 + 2?", 
     "answers": {"A": "3", "B": "4", "C": "5", "D": "6"}, "correct_answer": "4"},
    {"id": 2, "difficulty": "easy", "question": "What color is the sky on a clear day?", 
     "answers": {"A": "Blue", "B": "Green", "C": "Red", "D": "Yellow"}, "correct_answer": "Blue"},
    {"id": 3, "difficulty": "easy", "question": "What is the opposite of 'hot'?", 
     "answers": {"A": "Cold", "B": "Warm", "C": "Cool", "D": "Freezing"}, "correct_answer": "Cold"},
    {"id": 4, "difficulty": "easy", "question": "What does a cow say?", 
     "answers": {"A": "Meow", "B": "Bark", "C": "Moo", "D": "Quack"}, "correct_answer": "Moo"},
    {"id": 5, "difficulty": "easy", "question": "Which planet do we live on?", 
     "answers": {"A": "Mars", "B": "Venus", "C": "Earth", "D": "Jupiter"}, "correct_answer": "Earth"},
    {"id": 6, "difficulty": "medium", "question": "What is the capital of Japan?", 
     "answers": {"A": "Tokyo", "B": "Kyoto", "C": "Osaka", "D": "Hokkaido"}, "correct_answer": "Tokyo"},
    {"id": 7, "difficulty": "medium", "question": "What element does 'O' represent on the periodic table?", 
     "answers": {"A": "Oxygen", "B": "Osmium", "C": "Opal", "D": "Ozone"}, "correct_answer": "Oxygen"},
    {"id": 8, "difficulty": "medium", "question": "Who painted the Mona Lisa?", 
     "answers": {"A": "Vincent van Gogh", "B": "Leonardo da Vinci", "C": "Pablo Picasso", "D": "Claude Monet"}, "correct_answer": "Leonardo da Vinci"},
    {"id": 9, "difficulty": "medium", "question": "How many days are there in a leap year?", 
     "answers": {"A": "365", "B": "366", "C": "364", "D": "367"}, "correct_answer": "366"},
    {"id": 10, "difficulty": "medium", "question": "What is the largest ocean on Earth?", 
     "answers": {"A": "Atlantic", "B": "Pacific", "C": "Indian", "D": "Arctic"}, "correct_answer": "Pacific"},
    {"id": 11, "difficulty": "hard", "question": "Who developed the theory of general relativity?", 
     "answers": {"A": "Isaac Newton", "B": "Albert Einstein", "C": "Nikola Tesla", "D": "Stephen Hawking"}, "correct_answer": "Albert Einstein"},
    {"id": 12, "difficulty": "hard", "question": "What is the capital of Iceland?", 
     "answers": {"A": "Reykjavik", "B": "Oslo", "C": "Copenhagen", "D": "Stockholm"}, "correct_answer": "Reykjavik"},
    {"id": 13, "difficulty": "hard", "question": "What is the square root of 289?", 
     "answers": {"A": "16", "B": "17", "C": "18", "D": "19"}, "correct_answer": "17"},
    {"id": 14, "difficulty": "hard", "question": "Which gas is most abundant in Earth's atmosphere?", 
     "answers": {"A": "Oxygen", "B": "Hydrogen", "C": "Nitrogen", "D": "Carbon Dioxide"}, "correct_answer": "Nitrogen"},
    {"id": 15, "difficulty": "hard", "question": "What is the chemical formula for table salt?", 
     "answers": {"A": "NaCl", "B": "KCl", "C": "CaCl2", "D": "MgCl2"}, "correct_answer": "NaCl"}
]

@switch_question_bp.route('/help/switch_question', methods=['POST'])
def switch_question():
    # Get question data from client
    data = request.json
    current_question_id = data.get('current_question_id')
    current_difficulty = data.get('current_difficulty')

    if not current_question_id or not current_difficulty:
        return jsonify({"error": "Missing current_question_id or current_difficulty"}), 400

    # Filter valid questions by difficulty and remove current question
    valid_questions = [
        q for q in QUESTIONS 
        if q["difficulty"] == current_difficulty and q["id"] != current_question_id
    ]

    if not valid_questions:
        return jsonify({"error": "No more available questions for difficulty '{}'.".format(current_difficulty)}), 400

    # Select new random question
    new_question = random.choice(valid_questions)

    return jsonify({"new_question": new_question})