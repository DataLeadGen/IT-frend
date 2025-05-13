import os
import logging
import datetime
from flask import Flask
from flask_mail import Mail

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure Flask-Mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'info@theitfrnd.com')

# Initialize Flask-Mail
mail = Mail(app)

# Add custom Jinja filters
@app.template_filter('now')
def now_filter(format_string):
    if format_string == 'year':
        return datetime.datetime.now().year
    return datetime.datetime.now().strftime(format_string)
