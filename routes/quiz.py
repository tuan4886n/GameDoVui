from flask import Blueprint, jsonify
import requests

quiz_bp = Blueprint("quiz", __name__)

def fetch_questions_by_difficulty(difficulty, amount=5):
    url = f"https://the-trivia-api.com/api/questions?limit={amount}&difficulty={difficulty}"
    print(f"Requesting URL: {url}")
    
    try:
        response = requests.get(url, timeout=3)
        data = response.json()
        
        if response.status_code == 200 and isinstance(data, list) and len(data) > 0:
            return data
        else:
            print(f"Error: API returned empty results for {difficulty}")
            return []
    
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return []

@quiz_bp.route("/quiz", methods=["GET"])
def get_quiz():
    easy_questions = fetch_questions_by_difficulty("easy", 5)
    medium_questions = fetch_questions_by_difficulty("medium", 5)
    hard_questions = fetch_questions_by_difficulty("hard", 5)

    return jsonify({"quiz": easy_questions + medium_questions + hard_questions})