from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
app = Flask(__name__)

# -------------------------------
# Step 1: Create a small dataset
# -------------------------------

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
        "result": "Spam" if prediction == "spam" else "Not Spam"
    })

# -------------------------------
# Step 4: Home route
# -------------------------------
@app.route("/",methods=['POST','GET'])
def home():
    return render_template('index.html');

# -------------------------------
# Run app
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)