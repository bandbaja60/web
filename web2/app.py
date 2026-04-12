from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

app = Flask(__name__)

# -------------------------------
# OPTION 1: Load Pretrained Model
# (Uncomment this when you have .pkl files)
# -------------------------------
# model = pickle.load(open("spam_model.pkl", "rb"))
# vectorizer = pickle.load(open("vectorizer.pkl", "rb"))


# -------------------------------
# OPTION 2: Train Dummy Model
# -------------------------------

# Dummy dataset
messages = [
    "Win a free lottery now",
    "Claim your free prize",
    "Congratulations you won cash",
    "Free entry in a contest",
    "Call now to win money",

    "Hey how are you doing",
    "Let's meet tomorrow",
    "Are you coming to class",
    "Please review the document",
    "Lunch at 2 pm?"
]

labels = [
    "spam", "spam", "spam", "spam", "spam",
    "ham", "ham", "ham", "ham", "ham"
]

# Create vectorizer and model
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(messages)
print(X);
model = MultinomialNB()
model.fit(X, labels)

print(" Dummy model trained successfully")


# -------------------------------
# Prediction API
# -------------------------------
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
        "result": "Spam" if prediction == "spam" else "Not Spam"
    })


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)