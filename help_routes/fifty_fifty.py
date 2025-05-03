from flask import Blueprint, jsonify, request 
import random

help_bp = Blueprint('help', __name__)

@help_bp.route('/help/50-50', methods=['POST'])
def fifty_fifty():
    # get question data from client

    data = request.json
    correct_answer = data.get('correct_answer')
    all_answers = data.get('all_answers')

    if not correct_answer or not all_answers:
        return jsonify({"error": "Missing correct_answer or all_answers"}), 400

    # Logic: Eliminate 2 wrong answers, keep 1 correct + 1 random wrong answer

    remaining_choices = [correct_answer]
    wrong_answers = [ans for ans in all_answers if ans != correct_answer]
    remaining_choices.append(random.choice(wrong_answers))

    #shuffle to random order

    random.shuffle(remaining_choices)

    return jsonify({"remaining_choices": remaining_choices})