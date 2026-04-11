from flask import Flask, render_template, request

app = Flask(__name__)

# Dictionary-based responses
responses = {
    "hello": "Hi there!",
    "hi": "Hello!",
    "how are you": "I'm just a bot, but I'm fine!",
    "name": "I am a Flask chatbot.",
    "bye": "Goodbye! Have a great day!",
    "thanks": "You're welcome!"
}

def get_bot_response(user_input):
    user_input = user_input.lower()

    for key in responses:
        if key in user_input:
            return responses[key]

    return "Sorry, I didn't understand that."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot():
    user_msg = request.form["msg"]
    return get_bot_response(user_msg)

if __name__ == "__main__":
    app.run(debug=True)