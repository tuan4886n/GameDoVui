from flask import Blueprint, jsonify
import requests

quiz_bp = Blueprint("quiz", __name__)

def fetch_questions_by_difficulty(difficulty, amount=5):
    url = f"https://the-trivia-api.com/api/questions?limit={amount}&difficulty={difficulty}"
    
    try:
        response = requests.get(url, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                return data[:amount]  # Giới hạn số lượng chính xác
            else:
                print(f"Error: API returned empty results for {difficulty}")
        else:
            print(f"API responded with status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
    
    return []

@quiz_bp.route("/quiz", methods=["GET"])
def get_quiz():
    easy_questions = fetch_questions_by_difficulty("easy", 5)
    medium_questions = fetch_questions_by_difficulty("medium", 5)
    hard_questions = fetch_questions_by_difficulty("hard", 5)

    all_questions = (easy_questions[:5] + medium_questions[:5] + hard_questions[:5])[:15]  # Giới hạn đúng 15 câu

    print(f"Total questions fetched after limiting: {len(all_questions)}")  

    return jsonify({"quiz": all_questions})