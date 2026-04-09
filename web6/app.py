from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from textblob import TextBlob

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('comment')
def analyze_sentiment(data):
    comment = data['text']
    analysis = TextBlob(comment)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        sentiment = "Positive 😊"
    elif polarity < 0:
        sentiment = "Negative 😞"
    else:
        sentiment = "Neutral 😐"

    emit('sentiment_result', {'sentiment': sentiment})

if __name__ == '__main__':
    socketio.run(app, debug=True)
