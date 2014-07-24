from flask_oauthlib.client import OAuth
from flask import Flask, render_template, redirect, jsonify, request, flash, url_for, session
import jinja2
import tabledef
import search
from tabledef import User, MentoreeTopic, Topic
import linkedin
from xml.dom.minidom import parseString
from Project import app
import json

app.debug = True
app.secret_key = 'iLoveHelloKitty'

# main is for rendering templates. call function and render,
# post request will have topics ur looking for. send those topics as a parameter to search function. search function in search will do database query. 
# it will return a json of a list of mentors that have that topics.
# then return this list to the searchresults template to render

@app.route('/')
def index():
    if 'linkedin_token' in session:
        me = linkedin.linkedin.get('people/~')
        jsonify(me.data)
        # linkedin_data = json.loads(linkedin_json_string)
       
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/additionalinfo', methods=["GET"])
def addinfo_page():
    return render_template('additionalinfo.html')

@app.route('/additionalinfo', methods=["POST"])
def addinfo():
    mentoree_choice = request.form.get('mentoree-radios')
    age_range = request.form.get('agerange')
    gender_input = request.form.get('gender_radios')
    description_input = request.form.get('description')
    mentor_topics = request.form.getlist('mentortopics')

    linkedin.save_additional_user_data(mentoree_choice, age_range, gender_input, description_input, mentor_topics)
    # current_user = tabledef.dbsession.query(tabledef.User).filter_by(linkedintoken=session['linkedin_token']).first()
    return redirect(url_for('index'))

@app.route('/login')
def login():
    return linkedin.linkedin.authorize(callback=url_for('get_linkedin_data', _external=True))

@app.route('/logout')
def logout():
    session.pop('linkedin_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
@linkedin.linkedin.authorized_handler
def get_linkedin_data(resp):    

    user_json = linkedin.authorized(resp)
    user_json = user_json.data
    user_string = json.loads(user_json)

    user = tabledef.dbsession.query(tabledef.User).filter_by(linkedin_id=user_string["id"]).first()
    if user and user.new_user:
        return redirect(url_for('addinfo_page'))
    # print linkedin.authorize(callback=url_for('authorized', _external=True))

    return redirect(url_for('index'))

@app.route('/', methods=["POST"])
def search_results():
    mentee_topic_choice = request.form.get('searchtopics')

    mentor_data = search.search(mentee_topic_choice)
    search_topic = search.search_topic_display(mentee_topic_choice)
    print "mentor_data[0].educations_field_of_study"
    print mentor_data[0].ment_user.educations[0].educations_field_of_study
    return render_template('searchresults.html', mentor_data=mentor_data, search_topic_display=search_topic)

# @app.route('/search_results', methods=["GET"])
# def search_results():
#     mentor_data = request.args['mentor_data']
#     return render_template('searchresults.html', mentor_data=mentor_data)


@app.route('/mentor_detail/<linkedin_id>', methods=["GET"])
def mentor_page(linkedin_id):
    ment_data = search.mentor_detail_display(linkedin_id)
    return render_template('mentor_detail.html', ment_data=ment_data)
#    