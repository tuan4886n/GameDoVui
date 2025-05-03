from flask import Blueprint, jsonify, request
from config.database import connect_db

game_bp = Blueprint("game", __name__)

@game_bp.route("/start_game", methods=["POST"])
def start_game():
    # Kết nối cơ sở dữ liệu
    conn, cursor = connect_db()
    if not conn:
        return jsonify({"status": "❌ Lỗi kết nối database!"})

    # Lấy dữ liệu từ yêu cầu POST
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"status": "❌ Thiếu tên người chơi!", "error": "Vui lòng cung cấp username để bắt đầu trò chơi."})

    try:
        # Kiểm tra xem người chơi có tồn tại không
        cursor.execute("SELECT COUNT(*) FROM scores WHERE username = %s", (username,))
        user_exists = cursor.fetchone()[0]

        if not user_exists:
            return jsonify({
                "status": "❌ Người chơi không tồn tại!",
                "error": "Hãy đăng ký trước khi bắt đầu trò chơi."
            })

        # Reset điểm hiện tại và tăng số lần chơi
        cursor.execute("""
            UPDATE scores
            SET current_game_score = 0, total_sessions = total_sessions + 1
            WHERE username = %s
        """, (username,))
        conn.commit()

        # Lấy giá trị cập nhật của total_sessions và điểm hiện tại
        cursor.execute("SELECT total_sessions, current_game_score FROM scores WHERE username = %s", (username,))
        result = cursor.fetchone()

        if not result:
            return jsonify({
                "status": "❌ Lỗi không xác định!",
                "error": "Không thể lấy dữ liệu người chơi sau khi cập nhật."
            })

        total_sessions, current_game_score = result

        return jsonify({
            "status": "✅ Điểm đã được reset, trò chơi mới bắt đầu!",
            "username": username,
            "current_game_score": current_game_score,
            "total_sessions": total_sessions
        })
    except Exception as e:
        conn.rollback()  # Hủy thay đổi nếu có lỗi
        return jsonify({"status": "❌ Lỗi khi cập nhật database!", "error": str(e)})
    finally:
        cursor.close()
        conn.close()