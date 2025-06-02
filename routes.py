import os
from flask import render_template, request, flash, redirect, url_for, jsonify
from app import app, mail
from forms import ContactForm
from flask_mail import Message

@app.route('/')
def index():
    app.logger.debug("Rendering index page")
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/sample-leads')
def sample_leads():
    return render_template('sample_leads.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        try:
            # Create email message to admin
            admin_msg = Message(
                subject=f"IT FRNDLeads Contact Form: {form.subject.data}",
                recipients=[os.environ.get('CONTACT_EMAIL', 'naeem@theitfrnd.com')],
                html=render_template('emails/contact_admin.html',
                                   name=form.name.data,
                                   email=form.email.data,
                                   subject=form.subject.data,
                                   message=form.message.data),
                body=f"""
New contact form submission from IT FRNDLeads website:

Name: {form.name.data}
Email: {form.email.data}
Subject: {form.subject.data}

Message:
{form.message.data}

---
This message was sent from the IT FRNDLeads contact form.
                """,
                sender=os.environ.get('MAIL_DEFAULT_SENDER', 'naeem@theitfrnd.com'),
                reply_to=form.email.data
            )
            
            # Create confirmation email to user
            user_msg = Message(
                subject="Thank you for contacting IT FRNDLeads",
                recipients=[form.email.data],
                html=render_template('emails/contact_confirmation.html',
                                   name=form.name.data,
                                   subject=form.subject.data,
                                   message=form.message.data),
                body=f"""
Dear {form.name.data},

Thank you for reaching out to IT FRNDLeads. We have received your message and will get back to you within 24 hours.

Your message details:
Subject: {form.subject.data}
Message: {form.message.data}

Best regards,
IT FRNDLeads Team
Email: naeem@theitfrnd.com
Phone: +91 786-987-4458

---
This is an automated confirmation email.
                """,
                sender=os.environ.get('MAIL_DEFAULT_SENDER', 'naeem@theitfrnd.com')
            )
            
            # Send both emails
            mail.send(admin_msg)
            mail.send(user_msg)
            
            app.logger.info(f"Contact form email sent successfully from {form.email.data}")
            flash('Your message has been sent successfully! We will get back to you within 24 hours.', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            app.logger.error(f"Error sending email: {str(e)}")
            flash('There was an error sending your message. Please try again later or contact us directly at naeem@theitfrnd.com', 'danger')
    
    return render_template('contact.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
