import tabledef
from tabledef import User, MentoreeTopic, Topic, Email, Endorsement
import requests
import sqlalchemy
from sqlalchemy import update
import datetime
from flask import Flask, render_template, redirect, jsonify, request, flash, url_for, session

# import pdb

def save_endorsement_info_to_database(sender, mentor, endorsement_title, endorsement_body):
    today = datetime.datetime.now()
    endorsement_info = tabledef.Endorsement(sender_id=sender, receiver_id=mentor, title=endorsement_title, endorsements_text=endorsement_body, sent_date=today)
    print "!!~~~!!^^^ endorsement_info info"
    print endorsement_info
    tabledef.dbsession.add(endorsement_info)
    return tabledef.dbsession.commit()

def get_endorsement_info_per_mentor(linkedin_id):
    endorsement_hist = tabledef.dbsession.query(Endorsement).filter_by(receiver_id=linkedin_id).all()
    for endorsements in endorsement_hist:
        print "!^^^^^^^^^^^^^^^^endorsement history!! ^^^^^^^^^^^^^^^^^^^^^"
        print endorsements.sender.picture_url
    return endorsement_hist

