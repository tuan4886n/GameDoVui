from flask import Blueprint, request, jsonify
from config.database import connect_db

score_bp = Blueprint("score", __name__)

@score_bp.route("/submit_score", methods=["POST"])
def submit_score():
    # Connect to the database
    conn, cursor = connect_db()
    if not conn:
        return jsonify({"status": "❌ Kết nối cơ sở dữ liệu thất bại!", "error": "Database connection failed."})

    # Retrieve data from the POST request
    data = request.json
    username = data.get("username")
    difficulty = data.get("difficulty")
    correct = data.get("correct")

    # Validate input data
    if not username or difficulty not in ['easy', 'medium', 'hard'] or correct is None:
        return jsonify({"status": "❌ Dữ liệu không hợp lệ!", "error": "Invalid input data. Please check your parameters."})

    try:
        # Kiểm tra người chơi tồn tại trong cơ sở dữ liệu
        cursor.execute("SELECT COUNT(*) FROM scores WHERE username = %s", (username,))
        user_exists = cursor.fetchone()[0]

        if not user_exists:
            return jsonify({"status": "❌ Người chơi không tồn tại!", "error": "User not found. Please register first."})

        # Ánh xạ điểm số dựa trên độ khó
        score_map = {"easy": 10, "medium": 20, "hard": 30}
        score = score_map[difficulty] if correct else 0

        # Cập nhật điểm hiện tại của người chơi
        cursor.execute("""
            UPDATE scores
            SET current_game_score = current_game_score + %s
            WHERE username = %s
        """, (score, username))

        # Lấy điểm hiện tại và điểm cao nhất
        cursor.execute("""
            SELECT current_game_score, highest_score
            FROM scores
            WHERE username = %s
        """, (username,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"status": "❌ Lỗi không xác định!", "error": "Failed to fetch user scores."})

        current_game_score, highest_score = result

        # Cập nhật điểm cao nhất nếu cần thiết
        if current_game_score > highest_score:
            cursor.execute("""
                UPDATE scores
                SET highest_score = %s
                WHERE username = %s
            """, (current_game_score, username))

        conn.commit()

        # Trả về phản hồi thành công với dữ liệu đầy đủ
        return jsonify({
            "status": "✅ Điểm đã được cập nhật!",
            "username": username,
            "current_game_score": current_game_score,
            "highest_score": max(current_game_score, highest_score)
        })
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "❌ Lỗi khi cập nhật điểm số!", "error": str(e)})
    finally:
        cursor.close()
        conn.close()

@score_bp.route("/leaderboard", methods=["GET"])
def leaderboard():
    conn, cursor = connect_db()
    if not conn:
        return jsonify({"status": "❌ Kết nối cơ sở dữ liệu thất bại!", "error": "Database connection failed."})

    try:
        # Lấy tổng số người chơi
        cursor.execute("SELECT COUNT(*) FROM scores")
        total_players = cursor.fetchone()[0]

        # Lấy tham số 'page' từ query string (mặc định là 1)
        page = int(request.args.get("page", 1))
        limit = 10  # Số người chơi mỗi trang
        offset = (page - 1) * limit

        # Lấy dữ liệu người chơi theo trang hiện tại
        cursor.execute("""
            SELECT username, highest_score, timestamp
            FROM scores
            ORDER BY highest_score DESC, timestamp ASC
            LIMIT %s OFFSET %s
        """, (limit, offset))
        players = cursor.fetchall()

        # Nếu không có dữ liệu, trả về danh sách rỗng
        if not players:
            return jsonify({
                "status": "✅ Thành công!",
                "total_players": total_players,
                "leaderboard": []  # Danh sách rỗng
            })

        # Định dạng dữ liệu leaderboard
        leaderboard_data = [
            {
                "username": row[0],
                "highest_score": row[1],
                "timestamp": row[2].strftime('%Y-%m-%d %H:%M:%S') if row[2] else "N/A"
            }
            for row in players
        ]

        # Trả về dữ liệu leaderboard
        return jsonify({
            "status": "✅ Thành công!",
            "total_players": total_players,
            "leaderboard": leaderboard_data
        })
    except Exception as e:
        return jsonify({"status": "❌ Lỗi khi lấy dữ liệu bảng xếp hạng!", "error": str(e)})
    finally:
        cursor.close()
        conn.close()