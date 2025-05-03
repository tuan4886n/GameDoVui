from flask import Blueprint, jsonify, request
import random

audience_bp = Blueprint('audience', __name__)

@audience_bp.route('/help/audience', methods=['POST'])
def ask_the_audience():
    # get question data from client
    data = request.json
    all_answers = data.get('all_answers')
    correct_answer = data.get('correct_answer')

    if not all_answers or not correct_answer:
        return jsonify({"error": "Missing all_answers or correct_answer"}), 400

    # select cases according to probability ratio of 30%/70%
    case = random.choices([1, 2], weights=[30, 70], k=1)[0]
    poll = {answer: 0 for answer in all_answers}  # Initialize all percentages as 0%

    if case == 1:
        # case 1: The highest percentage belongs to wrong answers
        wrong_answers = [ans for ans in all_answers if ans != correct_answer]
        top_wrong = random.choice(wrong_answers)  # Randomly pick one wrong answer
        poll[top_wrong] = random.randint(40, 90)  # Assign highest percentage (Random)
        remaining_percentage = 100 - poll[top_wrong]

        # Ensure valid percentage for the correct answer
        if remaining_percentage // 2 < 20:
            poll[correct_answer] = remaining_percentage  # Assign all remaining percentage to correct answer
        else:
            poll[correct_answer] = random.randint(20, remaining_percentage // 2)  # Assign second highest percentage
        remaining_percentage -= poll[correct_answer]

        for ans in wrong_answers:
            if ans != top_wrong:
                # Check if remaining percentage is too small
                if remaining_percentage <= 5:
                    poll[ans] = remaining_percentage  # Assign remaining percentage directly
                else:
                    # Ensure valid range for random.randint
                    poll[ans] = random.randint(5, min(remaining_percentage, max(remaining_percentage // (len(wrong_answers) - 1), 1)))
                remaining_percentage -= poll[ans]

    else:
        # case 2: The highest percentage belongs to the correct answer
        poll[correct_answer] = random.randint(40, 100)  # Assign highest percentage (Random)
        remaining_percentage = 100 - poll[correct_answer]

        # distribute the remaining percentage to incorrect answers
        wrong_answers = [ans for ans in all_answers if ans != correct_answer]
        for i, ans in enumerate(wrong_answers):
            # If it's the last answer, assign all remaining percentage
            if i == len(wrong_answers) - 1:
                poll[ans] = remaining_percentage
            else:
                # Ensure valid range for random.randint
                if remaining_percentage <= 5:
                    poll[ans] = remaining_percentage
                else:
                    poll[ans] = random.randint(5, min(remaining_percentage, max(remaining_percentage // len(wrong_answers), 1)))
                remaining_percentage -= poll[ans]

    # Ensure total percentage equals 100%
    total_percentage = sum(poll.values())
    if total_percentage < 100:
        for ans in poll:
            if poll[ans] > 0:  # Adjust one answer to make up the difference
                poll[ans] += 100 - total_percentage
                break

    return jsonify({"poll": poll})