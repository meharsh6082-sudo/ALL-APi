import os
import socket
from flask import Flask, request, jsonify, Response
import resend

app = Flask(__name__, static_folder=None)


def get_api_key():
    return os.getenv("RESEND_API_KEY") or "re_NuKaHP6n_Ekg1WtHHTYLWTBv9mgRW1uwk"


def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


@app.route("/")
def index():
    html_path = os.path.join(os.path.dirname(__file__), "test.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    local_ip = get_local_ip()
    html = html.replace("{{REMOTE_ADDR}}", f"http://{local_ip}:5000")
    return Response(html, mimetype="text/html")


@app.route("/send-request", methods=["POST"])
def send_request():
    data = request.get_json() or {}
    name = data.get("name", "Unknown")
    email = data.get("email", "unknown@example.com")
    subject = data.get("subject", "New contact request")
    message = data.get("message", "")

    resend.api_key = get_api_key()
    payload = {
        "from": "onboarding@resend.dev",
        "to": "meharsh6082@gmail.com",
        "subject": f"Contact Request: {subject}",
        "html": f"<p><strong>Name:</strong> {name}</p>"
                f"<p><strong>Email:</strong> {email}</p>"
                f"<p><strong>Message:</strong><br>{message}</p>"
    }

    try:
        response = resend.Emails.send(payload)
        return jsonify({"status": "sent", "response": response})
    except Exception as exc:
        return jsonify({"status": "error", "error": str(exc)}), 500


if __name__ == "__main__":
    local_ip = get_local_ip()
    print(f"Server is running on http://127.0.0.1:5000")
    print(f"Open from other devices at http://{local_ip}:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
