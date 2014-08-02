import tabledef
from tabledef import User, MentoreeTopic, Topic, Email
import requests
import sqlalchemy
from sqlalchemy import update
import datetime
# import pdb


def save_email_info_to_database(sender, mentor, subject, subject_body):
    today = datetime.datetime.now()
    email_info = tabledef.Email(sender_id=sender, receiver_id=mentor, subject=subject, text_body=subject_body, sent_date=today)
    print "!!~~~!!^^^ email info"
    print email_info
    tabledef.dbsession.add(email_info)
    return tabledef.dbsession.commit()


def send_email(sender_email, mentor_email, subject, subject_body):

    return requests.post(
        "https://api.mailgun.net/v2/app27934969.mailgun.org/messages",
        auth=("api", "key-21q1narswc35vqr1u3f9upn3vf6ncbb9"),
        data={"from": mentor_email,
              "to": sender_email,
              "subject": subject,
              "text": subject_body})


# def send_email(sender_email, mentor_email, subject, subject_body):

#     return requests.post(
#         "https://api.mailgun.net/v2/app27934969.mailgun.org/messages",
#         auth=("api", "key-21q1narswc35vqr1u3f9upn3vf6ncbb9"),
#         data={"from": "Excited User <me@samples.mailgun.org>",
#               "to": "daphnejwang@gmail.com",
#               "subject": "Hello",
#               "text": "Testing some Mailgun awesomness!"})