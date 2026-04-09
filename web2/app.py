from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

# Load trained model and vectorizer
model = pickle.load(open("spam_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message field is required"}), 400

    message = data["message"]
    message_vec = vectorizer.transform([message])
    prediction = model.predict(message_vec)[0]

    return jsonify({
        "input_message": message,
        "prediction": prediction,
        "result": "Spam " if prediction == "spam" else "Not Spam "
    })

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
