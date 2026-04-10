from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer #
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
    # Get JSON data sent from frontend (e.g., {"id": 2})
    product = request.get_json()
    
    # Extract product ID from request
    product_id = product.get('id', '')
    
    # Find the index (position) of the product in the list
    # Needed because TF-IDF matrix works with index, not ID
    index = None
    for i in range(len(products)):
        if products[i]['id'] == product_id:
            index = i

    # If product not found, return empty list
    if index is None:
        return jsonify([])

    # 🤖 AI PART STARTS HERE

    # Compute cosine similarity between selected product and all products
    # Uses :contentReference[oaicite:0]{index=0}
    # tfidf_matrix[index] → selected product vector
    # tfidf_matrix → all product vectors
    similarity = cosine_similarity(tfidf_matrix[index], tfidf_matrix)

    # Convert similarity scores into (index, score) pairs
    # Example: [(0,1.0), (1,0.9), (2,0.85)...]
    scores = list(enumerate(similarity[0]))

    # Sort products based on similarity score (highest first)
    # x[1] = similarity value
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    # Prepare final recommendation list
    recommendations = []
    # Skip first item (it is the same product → similarity = 1.0)
    # Take next 3 most similar products
    for i in scores[1:4]:
        # i[0] = index of product
        # Add that product to recommendations
        recommendations.append(products[i[0]])

    # Return recommended products as JSON response
    return jsonify(recommendations)


if __name__ == '__main__':
    # Run Flask app in debug mode (auto reload + error logs)
    app.run(debug=True)