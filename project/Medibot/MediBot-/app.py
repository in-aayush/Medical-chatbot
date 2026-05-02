from flask import Flask, render_template, request, jsonify
from src.helper import get_answer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    response = get_answer(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)