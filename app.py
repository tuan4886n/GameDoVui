from flask import Flask
from config.database import connect_db
from routes.auth import auth_bp
from routes.score import score_bp
from routes.quiz import quiz_bp
from help_routes.fifty_fifty import help_bp
from help_routes.phone import phone_bp
from help_routes.audience import audience_bp
from help_routes.switch_question import switch_question_bp
from routes.start_game import game_bp
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS to allow frontend access to API
CORS(app, origins=["https://gamedovui.pages.dev"])

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
app.register_blueprint(help_bp)
app.register_blueprint(phone_bp)
app.register_blueprint(audience_bp)
app.register_blueprint(switch_question_bp)
app.register_blueprint(game_bp)

if __name__ == "__main__":
    app.run(debug=True)