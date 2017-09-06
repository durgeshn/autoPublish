import os
import smtplib
from config import config
# os.environ['DEBUG'] = '1'

def send_mail(mail_sub='', mail_body='', sender='', receivers=list()):
    # we need the receivers.
    if not receivers:
        return 'No receivers found, aborting mailing process.'

    # if no senders specified then take the local user as the sender.
    if not sender:
        user_name = os.environ['USERNAME']
        sender = '%s@mail.pcgi.com' % user_name
    if not mail_sub or not mail_body:
        return 'No Subject or the mail body provided, aborting mailing process.'
    message = 'From: %s\nTo: %s\nSubject: %s\n%s.' % (sender, receivers[0], mail_sub, mail_body)
    try:
        smtp_obj = smtplib.SMTP(config.mailHost)
        smtp_obj.sendmail(sender, receivers, message)
        smtp_obj.quit()
        print "Successfully sent email", '<--------------------------------'
    except smtplib.SMTPException:
        print "Error: unable to send email"
