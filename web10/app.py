from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

# Training data
texts = [
    "login user password",
    "buy product online",
    "view account details",
    "update profile info",
    "search products",
    "checkout cart",
    "customer support request",
    "browse homepage",
    "add item to wishlist",
    "reset password request",
    "SELECT * FROM users",
    "DROP TABLE users",
    "' OR 1=1 --",
    "<script>alert('hack')</script>",
    "../../etc/passwd"
]

labels = [
    "safe",
    "safe",
    "safe",
    "safe",
    "safe",
    "safe",
    "safe",
    "safe",
    "safe",
    "safe",
    "attack",
    "attack",
    "attack",
    "attack",
    "attack"
]
# Train model
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    text = request.json['text']
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]

    if prediction == "attack":
        result = "⚠️ Attack Detected"
    else:
        result = "✅ Safe"

    return jsonify({"status": result})

if __name__ == '__main__':
    app.run(debug=True)