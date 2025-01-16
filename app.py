from flask import Flask, request, render_template, session, jsonify
from flask_session import Session
from chatbots import abby_chat, katherine_chat, alex_chat

app = Flask(__name__)
app.secret_key = "DaGBAV57Skg20dgcDgbB2KQ3cZKDpSpD"  # Replace with a secure key
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    session.setdefault("chat_history", [])
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    persona = request.form.get('persona')
    user_message = request.form.get('message', '').strip()

    if not persona or not user_message:
        return jsonify({"error": "Missing persona or message"}), 400

    try:
        bot_response = {
            "Abby": abby_chat,
            "Katherine": katherine_chat,
            "Alex": alex_chat,
        }.get(persona, lambda x: "Unknown persona selected.")(user_message)

        chat_entry = {"user": user_message, "bot": bot_response}
        session["chat_history"].append(chat_entry)
        session.modified = True
        return jsonify({"chat_history": session["chat_history"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear_chat():
    session["chat_history"] = []
    session.modified = True
    return jsonify({"message": "Chat history cleared."})

if __name__ == '__main__':
    app.run(debug=True)