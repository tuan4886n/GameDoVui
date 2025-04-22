from flask import Blueprint, request, jsonify
from config.database import connect_db

score_bp = Blueprint("score", __name__)
@score_bp.route("/submit_score", methods=["POST"])
def submit_score():
    conn, cursor = connect_db()
    if not conn:
        return jsonify({"status":"❌ Lỗi kết nối database!"})

    data = request.json
    username = data.get("username")
    score = data.get("score")

    # Check input data
    if not username or not isinstance(score, int):
        return jsonify({"status": "❌ Dữ liệu không hợp lệ!"})

    cursor.execute("INSERT INTO scores (username, score) VALUES (%s, %s)", (username,score))
    conn.commit()

    return jsonify({"status": "✅ Điểm đã được lưu!", "username": username, "score": score})


@score_bp.route("/leaderboard", methods=["GET"])
def leaderboard():
    conn, cursor = connect_db()
    if not conn:
        return jsonify({"status": "❌ Lỗi kết nối database!"})

    cursor.execute("SELECT username, score, timestamp FROM scores ORDER BY score DESC, timestamp ASC LIMIT 10;")
    top_layers = cursor.fetchall()

    leaderboard_data = [{"username": row[0], "score": row[1], "timestamp": row[2].strftime('%Y-%m-%d %H:%M:%S')} for row in top_layers]

    return jsonify({"leaderboard": leaderboard_data})