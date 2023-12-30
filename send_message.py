import smtplib, ssl, os



def send_msg(msg):
    gmail = 'smtp.gmail.com'
    port = 465

    uname = 'learnpython407@gmail.com'
    pw = os.getenv('APP_PW')

    receiver = 'learnpython407@gmail.com'
    context = ssl.create_default_context()

    band, city, date = msg.split(',')

    message = f'''\
Subject: New Tour Found 

    Band: {band}
    City: {city}
    Date: {date}
    '''

    with smtplib.SMTP_SSL(gmail, port, context=context) as server:
        server.login(uname, pw)
        server.sendmail(uname, receiver, message)
    
    print(f'Message sent...')