from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Product data
products = [
    {"id": 1, "name": "Laptop high performance electronics"},
    {"id": 2, "name": "Smartphone mobile electronics"},
    {"id": 3, "name": "Wireless headphones electronics"},
    {"id": 4, "name": "Men shirt clothing"},
    {"id": 5, "name": "Blue jeans clothing"},
    {"id": 6, "name": "Winter jacket clothing"}
]

# Prepare TF-IDF
texts = [p["name"] for p in products]
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(texts)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json['query']

    # Convert query to vector
    query_vec = vectorizer.transform([query])

    # Compute similarity
    similarity = cosine_similarity(query_vec, tfidf_matrix)

    scores = list(enumerate(similarity[0]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    results = []
    for i in scores[:3]:  # top 3 results
        results.append(products[i[0]])

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)