import tabledef
from tabledef import User, MentoreeTopic, Topic, Email
import requests
import sqlalchemy
from sqlalchemy import update
import datetime
from flask import Flask, render_template, redirect, jsonify, request, flash, url_for, session

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
        data={"from": sender_email,
              "to": mentor_email,
              "subject": subject,
              "text": subject_body})

def get_email_history_per_mentor(linkedin_id):
    email_hist = tabledef.dbsession.query(Email).filter_by(sender_id=session['linkedin_id']).filter_by(receiver_id=linkedin_id).all()
    return email_hist

def get_sent_email_history_per_sender():
    email_hist = tabledef.dbsession.query(Email).filter_by(sender_id=session['linkedin_id']).all()
    return email_hist

def get_email_history():
    email_hist = tabledef.dbsession.query(Email).filter_by(receiver_id=session['linkedin_id']).all()
    for mail in email_hist:
        print "~!@#$%^&*( email history!! !@#$%^&"
        print mail.subject
    return email_hist

def get_email_with_id(email_id):
    email_id = tabledef.dbsession.query(Email).filter_by(id=email_id).all()
    eid = email_id[0]
    return eid

def format_json(row):
    formatted_json_dict={}
    for column in row.__table__.columns:
        formatted_json_dict[column.name] = str(getattr(row, column.name))
    return formatted_json_dict

def delete_email(id):
    deleted_email=tabledef.dbsession.query(Email).filter_by(id=id).first()
    tabledef.dbsession.delete(deleted_email)
    tabledef.dbsession.commit()
#     return requests.post(
#         "https://api.mailgun.net/v2/app27934969.mailgun.org/messages",
#         auth=("api", "key-21q1narswc35vqr1u3f9upn3vf6ncbb9"),
#         data={"from": "Excited User <me@samples.mailgun.org>",
#               "to": "daphnejwang@gmail.com",
#               "subject": "Hello",
#               "text": "Testing some Mailgun awesomness!"})