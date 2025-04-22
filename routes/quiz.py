from flask import Blueprint, jsonify
import requests

quiz_bp = Blueprint("quiz", __name__)

def fetch_all_questions():
    url = "https://opentdb.com/api.php?amount=20&type=multiple"
    
    try:
        response = requests.get(url, timeout=3)
        data = response.json()
        print("API Response:", data)
        
        if response.status_code == 200 and "results" in data and len(data["results"]) > 0:
            return data["results"]
        else:
            print("Error: API returned empty results")
            return []
    
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return []

@quiz_bp.route("/quiz", methods=["GET"])
def get_quiz():
    questions = fetch_all_questions()

    # Retry if API returns empty results
    retry_attempts = 3
    while len(questions) < 20 and retry_attempts > 0:
        print("Retrying API request...")
        questions = fetch_all_questions()
        retry_attempts -= 1

    easy_questions = [q for q in questions if q["difficulty"] == "easy"][:5]
    medium_questions = [q for q in questions if q["difficulty"] == "medium"][:5]
    hard_questions = [q for q in questions if q["difficulty"] == "hard"][:5]
    extreme_questions = hard_questions[:5]

    return jsonify({"quiz": easy_questions + medium_questions + hard_questions + extreme_questions})