from flask import Flask, render_template, request
import random

app = Flask(__name__)

USER = {"username": "admin", "password": "1234"}
current_otp = ""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    global current_otp

    username = request.form.get('username')
    password = request.form.get('password')

    if username == USER['username'] and password == USER['password']:
        current_otp = str(random.randint(1000, 9999))
        return f"OTP Generated: {current_otp}"  # ⚠️ insecure (see below)
    else:
        return "Invalid Credentials"

@app.route('/verify', methods=['POST'])
def verify():
    global current_otp

    otp = request.form.get('otp')

    if otp == current_otp:
        return "Login Successful"
    else:
        return "Wrong OTP"

if __name__ == '__main__':
    app.run(debug=True)