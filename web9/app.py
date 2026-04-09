from flask import Flask, render_template, request
import pyttsx3
import speech_recognition as sr

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():

    text = ""

    if request.method == "POST":

        action = request.form["action"]

        # TEXT TO SPEECH
        if action == "speak":
            text = request.form["text"]
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()

        # SPEECH TO TEXT
        elif action == "listen":
            r = sr.Recognizer()

            try:
                with sr.Microphone() as source:
                    print("Speak now...")
                    audio = r.listen(source)

                text = r.recognize_google(audio)

            except sr.UnknownValueError:
                text = "Could not understand audio"

            except sr.RequestError:
                text = "Internet connection problem"

    return render_template("index.html", text=text)

if __name__ == "__main__":
    app.run(debug=True)