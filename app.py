from flask import Flask, jsonify
import requests
from config.database import connect_db
from routes.auth import auth_bp


app = Flask(__name__)

@app.route("/test_db", methods=["GET"])
def test_db():
    conn, cursor = connect_db()
    if conn:
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        return {"status": "✅ Kết nối PostgreSQL thành công!", "users": users}
    else:
        return {"status": "❌ Kết nối thất bại!"}

app.register_blueprint(auth_bp)

def fetch_all_questions():

    url = "https://opentdb.com/api.php?amount=20&type=multiple"
    
    try:
        response = requests.get(url, timeout=3)  # API request with timeout
        data = response.json()  # Convert response to JSON
        print("API Response:", data)  # Debugging log
        
        if response.status_code == 200 and "results" in data and len(data["results"]) > 0:
            return data["results"]
        else:
            print("Error: API returned empty results")
            return []  # Return empty list if API fails
    
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")  # Log API failure
        return []

@app.route("/quiz", methods=["GET"])
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

if __name__ == "__main__":
    app.run(debug=True)