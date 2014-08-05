from flask_oauthlib.client import OAuth
from flask import Flask, render_template, redirect, jsonify, request, flash, url_for, session
import jinja2
import tabledef
from tabledef import *
from sqlalchemy import update
from xml.dom.minidom import parseString
import os
import urllib
import json
from Project import app
import pdb
from tabledef import User

oauth = OAuth(app)

linkedin = oauth.remote_app(
    'linkedin',
    consumer_key='75ifkmbvuebxtg',
    consumer_secret='LAUPNTnEbsBu7axq',
    request_token_params={
        'scope': 'r_fullprofile,r_basicprofile,r_emailaddress',
        'state': 'RandomString',
    },
    base_url='https://api.linkedin.com/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
    authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
)


def authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['linkedin_token'] = (resp['access_token'], '')
    linkedin_json_string = linkedin.get('people/~:(id,first-name,last-name,industry,headline,site-standard-profile-request,certifications,educations,summary,specialties,positions,picture-url,email-address)')
    session['linkedin_id'] = linkedin_json_string.data['id']
    
    tabledef.import_linkedin_user(linkedin_json_string.data)
    return jsonify(linkedin_json_string.data)


@linkedin.tokengetter
def get_linkedin_oauth_token():
    return session.get('linkedin_token')

# def get_linkedin_id():
#     return session.get('linkedin_id')

def change_linkedin_query(uri, headers, body):
    auth = headers.pop('Authorization')
    headers['x-li-format'] = 'json'
    if auth:
        auth = auth.replace('Bearer', '').strip()
        if '?' in uri:
            uri += '&oauth2_access_token=' + auth
        else:
            uri += '?oauth2_access_token=' + auth
    return uri, headers, body

def save_additional_user_data(mentoree_choice, age_range, gender_input, description_input, mentor_topics):
    tabledef.dbsession.query(tabledef.User).filter_by(linkedin_id=session['linkedin_id']).update({
        'mentor': mentoree_choice,
        'age':age_range,
        'gender':gender_input,
        'description':description_input,
        'new_user':False})

    for topics in mentor_topics:
        mentor_selected_topics = tabledef.MentoreeTopic(topic_id = topics, mentor_id=session['linkedin_id'])
        tabledef.dbsession.add(mentor_selected_topics)
    return tabledef.dbsession.commit()

def update_additional_user_data(mentoree_choice, age_range, gender_input, description_input, mentor_topics):
    user = tabledef.dbsession.query(User).filter_by(linkedin_id=session['linkedin_id']).first()

    user.mentor = mentoree_choice
    user.age = age_range
    user.gender = gender_input
    user.description = description_input

    current_selected_topics = tabledef.dbsession.query(tabledef.MentoreeTopic).filter_by(mentor_id=session['linkedin_id']).all()
    for curr_topics in current_selected_topics:
        tabledef.dbsession.delete(curr_topics)
    # pdb.set_trace()
    for topics in mentor_topics:
        mentor_selected_topics = tabledef.MentoreeTopic(topic_id = topics, mentor_id=session['linkedin_id'])
        tabledef.dbsession.add(mentor_selected_topics)

    return tabledef.dbsession.commit()

linkedin.pre_request = change_linkedin_query
