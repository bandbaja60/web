from flask import Flask, render_template, request, jsonify
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

    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    if username == USER['username'] and password == USER['password']:
        current_otp = str(random.randint(1000, 9999))
       
        print(f"Generated OTP: {current_otp}")

        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid Credentials'})

@app.route('/verify', methods=['POST'])
def verify():
    global current_otp

    data = request.get_json()
    otp = data.get('otp', '')

    if otp == current_otp:
        return jsonify({'success': True, 'message': 'Login Successful'})
    else:
        return jsonify({'success': False, 'message': 'Wrong OTP'})

if __name__ == '__main__':
    app.run(debug=True)