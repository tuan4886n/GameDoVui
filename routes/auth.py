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
        return jsonify({"status":"❌ Vui lòng nhập đầy đủ thông tin!"})
    # Encrypt password for security

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        cursor.execute("INSERT INTO users (username, password, score) VALUES (%s, %s, %s)", (username, hashed_password,0))
        conn.commit()
        return jsonify({"status": "✅ Đăng ký thành công!", "username": username})
    except Exception as e:
        return jsonify({"status": "❌ Lỗi đăng ký!", "error": str(e)})


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

    # Encrypt password to check with database
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
        user = cursor.fetchone()

        if user:
            return jsonify({"status": "✅ Đăng nhập thành công!", "username": username})
        else:
            return jsonify({"status": "❌ Sai tài khoản hoặc mật khẩu!"})
    except Exception as e:
        return jsonify({"status": "❌ Lỗi đăng nhập!", "error": str(e)})

