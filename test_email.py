#!/usr/bin/env python3
"""
Test script to verify SMTP email configuration
"""
import os
from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail, Message

# Load environment variables
load_dotenv()

# Create a simple Flask app for testing
app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'naeem@theitfrnd.com')

# Initialize Flask-Mail
mail = Mail(app)

def test_email():
    """Test sending an email"""
    with app.app_context():
        try:
            print("Testing SMTP configuration...")
            print(f"MAIL_SERVER: {app.config['MAIL_SERVER']}")
            print(f"MAIL_PORT: {app.config['MAIL_PORT']}")
            print(f"MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
            print(f"MAIL_DEFAULT_SENDER: {app.config['MAIL_DEFAULT_SENDER']}")
            
            # Create test message
            msg = Message(
                subject="IT FRNDLeads SMTP Test",
                recipients=[os.environ.get('CONTACT_EMAIL', 'naeem@theitfrnd.com')],
                body="""
This is a test email to verify that the SMTP configuration is working correctly.

If you receive this email, the SMTP setup is successful!

Best regards,
IT FRNDLeads System
                """,
                sender=os.environ.get('MAIL_DEFAULT_SENDER', 'naeem@theitfrnd.com')
            )
            
            # Send the email
            mail.send(msg)
            print("SUCCESS: Test email sent successfully!")
            return True
            
        except Exception as e:
            print(f"ERROR: Error sending test email: {str(e)}")
            return False

if __name__ == "__main__":
    test_email()