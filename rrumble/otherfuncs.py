from rrumble import app
from PIL import Image
import secrets
import os
import smtplib
import imghdr
from email.message import EmailMessage as EM

def photo_update(new_photo):
    phex= secrets.token_hex(8)
    _, f_ext = os.path.splitext(new_photo.filename)
    new_name = phex + f_ext
    new_loc = os.path.join(app.root_path, 'static/media/profphot', new_name)
    output = (640, 462)
    i = Image.open(new_photo)
    i.thumbnail(output)
    i.save(new_loc)
   
    return new_name

MAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
MAIL_PASS = os.environ.get('MAIL_APP_PASS')

def send_mail(subject, to, content, attachment=False):
    msg= EM()
    msg['Subject']= subject
    msg['From']= MAIL_ADDRESS
    msg['To'] = to
    msg.set_content(content)

    _, ext = os.path.splitext(attachment.filename)
    if ext=='jpg' or ext=='jpeg' or ext=='png':
        with open(attachment, 'rb') as attach:
            file = attach.read()
            file_name = attach.name
            file_type = imghdr.what(attach.name)
            msg.add_attachment(file, filename=file_name, maintype='image', subtype=file_type)
    
    elif ext == 'pdf':
        with open(attachment, 'rb') as attach:
            file = attach.read()
            file_name = attach.name
            msg.add_attachment(file, filename=file_name, maintype='application', subtype='octet-stream')


        with smtplib.SMTP_SSL('smpt.gmail.com', 465) as envoyer:
            envoyer.login(MAIL_ADDRESS, MAIL_PASS)
            envoyer.send_message(msg)
