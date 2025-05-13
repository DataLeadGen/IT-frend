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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        try:
            # Create email message
            msg = Message(
                subject=f"IT FRNDLeads Contact Form: {form.subject.data}",
                recipients=[os.environ.get('CONTACT_EMAIL', 'info@theitfrnd.com')],
                body=f"""
                Name: {form.name.data}
                Email: {form.email.data}
                Subject: {form.subject.data}
                
                Message:
                {form.message.data}
                """,
                sender=form.email.data
            )
            mail.send(msg)
            
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            app.logger.error(f"Error sending email: {str(e)}")
            flash('There was an error sending your message. Please try again later.', 'danger')
    
    return render_template('contact.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
