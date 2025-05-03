from flask import Blueprint, jsonify, request
import random

phone_bp = Blueprint('phone', __name__)

@phone_bp.route('/help/phone', methods=['POST'])
def phone_a_friend():
    
    # get question data from client
    data = request.json
    correct_answer = data.get('correct_answer')
    all_answers = data.get('all_answers')

    if not correct_answer or not all_answers:
        return jsonify({"error": "Missing correct_answer or all_answers"}), 400

    # Logic: random returns a hint (can be true or false)
    suggestion = random.choice(all_answers)

    # increase the chances of choosing correctly (ex: 70% is correct, 30% is wrong)
    if random.random() < 0.7:
        suggestion = correct_answer

    return jsonify({"suggestion": suggestion})
