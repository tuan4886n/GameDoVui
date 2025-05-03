from flask import Blueprint, request, jsonify
from config.database import connect_db
import hashlib

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    conn, cursor = connect_db()
    if not conn:
        return jsonify({"status": "❌ Lỗi kết nối database!"})

    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"status": "❌ Vui lòng nhập đầy đủ thông tin!"})

    # Mã hóa mật khẩu để tăng bảo mật
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        # Kiểm tra xem username đã tồn tại chưa
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({"status": "❌ Username đã tồn tại! Vui lòng chọn tên khác."})

        # Thêm người dùng vào bảng 'users'
        cursor.execute("INSERT INTO users (username, password, score) VALUES (%s, %s, %s)", (username, hashed_password, 0))
        
        # Thêm bản ghi vào bảng 'scores' cho người chơi với điểm khởi tạo
        cursor.execute("INSERT INTO scores (username, current_game_score, highest_score) VALUES (%s, %s, %s)", (username, 0, 0))

        conn.commit()  # Xác nhận các thay đổi trong cơ sở dữ liệu
        return jsonify({"status": "✅ Đăng ký thành công!", "username": username})
    except Exception as e:
        conn.rollback()  # Hủy các thay đổi nếu xảy ra lỗi
        return jsonify({"status": "❌ Lỗi đăng ký!", "error": str(e)})
    finally:
        cursor.close()
        conn.close()


@auth_bp.route("/login", methods=["POST"])
def login():
    conn, cursor = connect_db()
    if not conn:
        return jsonify({"status": "❌ Lỗi kết nối database!"})

    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"status": "❌ Vui lòng nhập đầy đủ thông tin!"})

    # Mã hóa mật khẩu để kiểm tra với cơ sở dữ liệu
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
        user = cursor.fetchone()

        if user:
            # Truy xuất điểm hiện tại từ bảng 'scores'
            cursor.execute("SELECT current_game_score, highest_score FROM scores WHERE username = %s", (username,))
            scores = cursor.fetchone()

            return jsonify({
                "status": "✅ Đăng nhập thành công!",
                "username": username,
                "current_score": scores[0] if scores else 0,
                "highest_score": scores[1] if scores else 0
            })
        else:
            return jsonify({"status": "❌ Sai tài khoản hoặc mật khẩu!"})
    except Exception as e:
        return jsonify({"status": "❌ Lỗi đăng nhập!", "error": str(e)})
    finally:
        cursor.close()
        conn.close()

