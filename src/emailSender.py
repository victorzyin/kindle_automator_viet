# http://linuxcursor.com/python-programming/06-how-to-send-pdf-ppt-attachment-with-html-body-in-python-script

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gethostname
from smtplib import SMTP


def send_email(path_to_pdf, book_name, subject, message, from_email, dest_email, password):
    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)

    msg = MIMEMultipart()

    message = f'{message}\nSend from Hostname: {gethostname()}'
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = dest_email

    msg.attach(MIMEText(message, "plain"))

    with open(path_to_pdf, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
    attach.add_header('Content-Disposition', 'attachment', filename=str(book_name))
    msg.attach(attach)

    server.send_message(msg)
