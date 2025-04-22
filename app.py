from flask import Flask
from config.database import connect_db
from routes.auth import auth_bp
from routes.score import score_bp
from routes.quiz import quiz_bp

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
app.register_blueprint(score_bp)
app.register_blueprint(quiz_bp)

if __name__ == "__main__":
    app.run(debug=True)