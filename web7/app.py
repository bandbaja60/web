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
product_texts = [p["name"] for p in products]
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(product_texts)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    product_id = request.json['id']
    
    index = None
    for i in range(len(products)):
        if products[i]['id'] == product_id:
            index = i

    if index is None:
        return jsonify([])

    # Compute similarity
    similarity = cosine_similarity(tfidf_matrix[index], tfidf_matrix)
    scores = list(enumerate(similarity[0]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommendations = []
    for i in scores[1:4]:  # top 3
        recommendations.append(products[i[0]])

    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)