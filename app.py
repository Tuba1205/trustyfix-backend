from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()  # load .env file

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

@app.route('/')
def home():
    return "Kitchen Repair API is running!"

@app.route('/api/send-email', methods=['POST'])
def send_email():
    data = request.json

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    street = data.get('street')
    phone = data.get('phone')
    city = data.get('city')
    state = data.get('state')
    zip_code = data.get('zip')

    # Email settings
    sender_email = os.environ.get("EMAIL_ADDRESS")
    sender_password = os.environ.get("EMAIL_PASSWORD")
    receiver_email = "umarsaleem818@gmail.com"  # where you want to receive form submissions

    subject = "New Contact Form Submission"
    body = f"""
    First Name: {first_name}
    Last Name: {last_name}
    Email: {email}
    Street: {street}
    Phone: {phone}
    City: {city}
    State: {state}
    Zip Code: {zip_code}
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)