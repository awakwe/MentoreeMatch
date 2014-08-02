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
from flask import redirect
import pagination
import email_module

app.debug = True
app.secret_key = 'iLoveHelloKitty'

# Pagination
PER_PAGE = 5

def url_for_other_page(page, mentee_topic_choice):
    args = dict(request.view_args.items() + request.args.to_dict().items()) 
    args['page'] = page
    args['mentee_topic_choice'] = mentee_topic_choice
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

@app.route('/')
def homepage():
    return render_template('home_page.html')

@app.route('/home')
def index():
    if 'linkedin_token' in session:
        me = linkedin.linkedin.get('people/~')
        jsonify(me.data)
        # linkedin_data = json.loads(linkedin_json_string)
        topics = tabledef.Topic.query.order_by("topic_id").all()
        return render_template('index.html', topics=topics)
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

@app.route('/home', defaults={'page': 1}, methods=["POST"])
@app.route('/home/page/<int:page>/<mentee_topic_choice>')
def search_results(page, mentee_topic_choice = None):
    mentee_topic_choice = mentee_topic_choice or request.form.get('searchtopics')
    mentor_data = search.search(mentee_topic_choice)

    start_index = (page - 1) * (PER_PAGE)
    end_index = (page) * (PER_PAGE)

    ment_count = len(mentor_data)
    users = mentor_data[start_index:end_index]
    # users = mentor_data.paginate(page, PER_PAGE, False)

    if not users and page != 1:
        abort(404)
    pagination_per_page = pagination.Pagination(page, PER_PAGE, ment_count)
    search_topic = search.search_topic_display(mentee_topic_choice)
    return render_template('searchresults.html', search_topic_display=search_topic, 
        pagination=pagination_per_page, users=users, mentee_topic_choice=mentee_topic_choice)


@app.route('/mentor_detail/<linkedin_id>', methods=["GET"])
def mentor_page(linkedin_id):
    ment_data = search.mentor_detail_display(linkedin_id)
    return render_template('mentor_detail.html', ment_data=ment_data)

@app.route('/profile', methods=["GET"])
def self_page():
    print "~!~!~!~!~ session linkedin_id"
    print session['linkedin_id'] 
    if 'linkedin_id' in session:
        ment_data = search.mentor_detail_display(session['linkedin_id'])
        return render_template('self_profile.html', ment_data=ment_data)
    return redirect(url_for('login'))

@app.route('/edit_profile', methods=["GET"])
def mentor_page_update():
    if 'linkedin_id' in session:
        ment_data = search.mentor_detail_display(session['linkedin_id'])
        ment_pers_topics = search.mentor_personal_topics(session['linkedin_id'])
        topics = tabledef.Topic.query.order_by("topic_id").all()
        return render_template('edit_self_profile.html', ment_data=ment_data, ment_pers_topics=ment_pers_topics, topics=topics)
    return redirect(url_for('login'))

@app.route('/edit_profile', methods=["POST"])
def mentor_page_update_post():
    mentoree_choice = request.form.get('mentoree-radios')
    age_range = request.form.get('agerange')
    gender_input = request.form.get('gender_radios')
    description_input = request.form.get('description')
    mentor_topics = request.form.getlist('mentortopics')

    linkedin.update_additional_user_data(mentoree_choice, age_range, gender_input, description_input, mentor_topics)
    return redirect(url_for('self_page'))


@app.route('/email/<linkedin_id>', methods=["GET"])
def email_get(linkedin_id):
    ment_data = search.mentor_detail_display(linkedin_id)
    user_data = search.mentor_detail_display(session['linkedin_id'])
    print "email GET ^^^^^^^^^^^^^^^^^^"
    print ment_data
    print user_data
    return render_template('email_form.html', ment_data=ment_data, user_data=user_data)

@app.route('/email', methods=["POST"])
def email_post():
    sender = session['linkedin_id']
    sender_data= search.mentor_detail_display(sender)
    sender_email = sender_data.email

    mentor = request.form.get('mentor_id')
    print "mentor"
    print mentor
    mentor_data = search.mentor_detail_display(mentor)
    mentor_email = mentor_data.email

    subject = request.form.get('subject')
    subject_body = request.form.get('message')
    print "^^^^^^^^^^^^^^^^^^ sender email, mentor email, subject body"
    print sender_email
    print mentor_email
    print subject_body

    email_module.save_email_info_to_database(sender, mentor, subject, subject_body)
    email_module.send_email(sender_email, mentor_email, subject, subject_body)

    messages = flash('Success! Your message has been sent successfully.')

    return redirect(url_for('email_get', linkedin_id=mentor, messages=messages))


   