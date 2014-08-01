#import tabledef
#from tabledef import User, MentoreeTopic, Topic
import requests
# import pdb

def save_email_to_database(sender_email, mentor_email, subject, subject_body):
    receiver = tabledef.dbsession.query(tabledef.User).filter_by(linkedin_id=linkedin_id).first()
    sender = tabledef.dbsession.query(User).filter_by(linkedin_id=session['linkedin_id']).first()

    sender_email = 


def send_email(sender_email, mentor_email, subject, subject_body):

    return requests.post(
        "https://api.mailgun.net/v2/app27934969.mailgun.org/messages",
        auth=("api", "key-21q1narswc35vqr1u3f9upn3vf6ncbb9"),
        data={"from": "Excited User <me@samples.mailgun.org>",
              "to": "daphnejwang@gmail.com",
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})