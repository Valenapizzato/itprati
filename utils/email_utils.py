from flask_mail import Message

def send_email(mail, subject, body, recipient):
    msg = Message(subject, sender=mail.username, recipients=[recipient])
    msg.body = body
    mail.send(msg)