#!/usr/bin/env python3
"""
Test script to verify contact form with SMTP functionality
"""
import os
from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail, Message
from app import app, mail
from forms import ContactForm

def test_contact_form_email():
    """Test the contact form email functionality"""
    with app.app_context():
        try:
            print("Testing contact form email functionality...")
            
            # Create a test form data
            test_data = {
                'name': 'Test User',
                'email': 'test@example.com',
                'subject': 'Test Contact Form Submission',
                'message': 'This is a test message to verify that the contact form email functionality is working correctly.'
            }
            
            # Create email message to admin (same as in routes.py)
            admin_msg = Message(
                subject=f"IT FRNDLeads Contact Form: {test_data['subject']}",
                recipients=[os.environ.get('CONTACT_EMAIL', 'naeem@theitfrnd.com')],
                body=f"""
New contact form submission from IT FRNDLeads website:

Name: {test_data['name']}
Email: {test_data['email']}
Subject: {test_data['subject']}

Message:
{test_data['message']}

---
This message was sent from the IT FRNDLeads contact form.
                """,
                sender=os.environ.get('MAIL_DEFAULT_SENDER', 'naeem@theitfrnd.com'),
                reply_to=test_data['email']
            )
            
            # Send the admin email
            mail.send(admin_msg)
            print("SUCCESS: Admin notification email sent successfully!")
            
            # Create confirmation email to user
            user_msg = Message(
                subject="Thank you for contacting IT FRNDLeads",
                recipients=[os.environ.get('CONTACT_EMAIL', 'naeem@theitfrnd.com')],  # Sending to admin for testing
                body=f"""
Dear {test_data['name']},

Thank you for reaching out to IT FRNDLeads. We have received your message and will get back to you within 24 hours.

Your message details:
Subject: {test_data['subject']}
Message: {test_data['message']}

Best regards,
IT FRNDLeads Team
Email: naeem@theitfrnd.com
Phone: +91 786-987-4458

---
This is an automated confirmation email.
                """,
                sender=os.environ.get('MAIL_DEFAULT_SENDER', 'naeem@theitfrnd.com')
            )
            
            # Send the user confirmation email
            mail.send(user_msg)
            print("SUCCESS: User confirmation email sent successfully!")
            
            print("\nContact form email functionality test completed successfully!")
            print("Check your email inbox for both the admin notification and user confirmation emails.")
            return True
            
        except Exception as e:
            print(f"ERROR: Error testing contact form email: {str(e)}")
            return False

if __name__ == "__main__":
    test_contact_form_email()