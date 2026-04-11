from flask import Flask,render_template,request
import tensorflow as tf

import numpy as np
from PIL import Image

app = Flask(__name__)

## Load the model
model = tf.keras.applications.MobileNetV2(weights='imagenet')


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    image = request.files["image"]

    img = Image.open(image).resize((224, 224))
    img_array = np.array(img)

    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    preds = model.predict(img_array)
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=1)

    prediction = decoded[0][0][1]

    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    app.run(debug=True)

    