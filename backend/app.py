from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db, init_db

app = Flask(__name__)
CORS(app)   # ⭐ IMPORTANT

# ─────────────────────────────
# SIGNUP
# ─────────────────────────────
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"status": "fail", "message": "⚠️ Fill all fields"})

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO Users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()

        return jsonify({"status": "success", "message": "✅ Signup successful"})

    except:
        return jsonify({"status": "fail", "message": "⚠️ Username already exists"})

    finally:
        conn.close()


# ─────────────────────────────
# LOGIN
# ─────────────────────────────
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM Users WHERE username=? AND password=?",
        (username, password)
    )

    user = cur.fetchone()
    conn.close()

    if user:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})


# ─────────────────────────────
# RUN
# ─────────────────────────────
if __name__ == "__main__":
    init_db()   # ⭐ creates table
    app.run(debug=True)