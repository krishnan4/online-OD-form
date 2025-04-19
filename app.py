from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Load environment variables
load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
print(f"EMAIL_ADDRESS: {EMAIL_ADDRESS}")
print(f"EMAIL_PASSWORD: {EMAIL_PASSWORD}")
SMTP_SERVER = 'smtp.gmail.com'  # Update for your email provider
SMTP_PORT = 587  # Update for your email provider

@app.route('/')
def index():
    return render_template('od_form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Collect form data
        student_id = request.form['studentId']
        student_name = request.form['studentName']
        department = request.form['department']
        email = request.form['email']
        no_of_days = request.form['noOfDays']
        leaving_time = request.form['leavingTime']
        return_time = request.form['returnTime']
        date = request.form['date']
        od_count = request.form['odCount']
        event_type = request.form['eventType']
        attending_university = request.form['attendingUniversity']

        # Basic validation
        if not student_id.isdigit() or len(student_id) != 8:
            flash('Student ID must be an 8-digit number.', 'error')
            return redirect(url_for('index'))
        if not department:
            flash('Please select a department.', 'error')
            return redirect(url_for('index'))
        if int(no_of_days) < 1:
            flash('Number of days must be at least 1.', 'error')
            return redirect(url_for('index'))
        if int(od_count) < 1:
            flash('OD count must be at least 1.', 'error')
            return redirect(url_for('index'))

        # Prepare email content
        subject = 'Student OD Form Submission'
        body = f"""
        Student OD Form Details:
        Student ID: {student_id}
        Student Name: {student_name}
        Department: {department}
        Email: {email}
        Number of Days: {no_of_days}
        Leaving Time: {leaving_time}
        Return Time: {return_time}
        Date: {date}
        OD Count: {od_count}
        Event Type: {event_type}
        Attending University: {attending_university}
        """

        # Set up email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = 'hariad109@rmkcet.ac.in'  # Replace with recipient email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, msg['To'], msg.as_string())
            flash('Form submitted successfully!', 'success')
        except smtplib.SMTPAuthenticationError:
            flash('Failed to send form: Invalid email address or password.', 'error')
        except smtplib.SMTPException as e:
            flash(f'Failed to send form: SMTP error - {str(e)}', 'error')
        except Exception as e:
            flash(f'Failed to send form: {str(e)}', 'error')

        return redirect(url_for('index'))

    except Exception as e:
        flash(f'Failed to send form: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)