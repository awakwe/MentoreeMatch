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
import endorsements

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

# LOGIN Pages
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

# HOME & ACCOUNT CREATION Pages
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


@app.route('/home', defaults={'page': 1}, methods=["POST"])
@app.route('/home/page/<int:page>/<mentee_topic_choice>')
def search_results(page, mentee_topic_choice = None):
    mentee_topic_choice = mentee_topic_choice or request.form.get('searchtopics')
    print "~~~~~~~~~~~~~~~~mentee_topic_choice"
    print mentee_topic_choice
    mentor_data = search.search(mentee_topic_choice)
    if mentor_data:

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
    messages = flash('Sorry! There are no mentors under this search topic')
    return redirect(url_for('index'))

# MENTOR DETAIL PAGES
@app.route('/mentor_detail/<linkedin_id>', methods=["GET"])
def mentor_page(linkedin_id):
    ment_data = search.mentor_detail_display(linkedin_id)
    user_data = search.mentor_detail_display(session['linkedin_id'])
    endorsement_history = endorsements.get_endorsement_info_per_mentor(linkedin_id)

    return render_template('mentor_detail.html', ment_data=ment_data, user_data=user_data, endorsement_history=endorsement_history)

@app.route('/mentor_detail', methods=["POST"])
def add_endorsement():
    sender = session['linkedin_id']
    sender_data= search.mentor_detail_display(sender)

    mentor = request.form.get('mentor_id')
    print "~~~~~~~~~~~~~~~~MENTOR ID on main"
    print mentor
    mentor_data = search.mentor_detail_display(mentor)

    endorsement_title = request.form.get('endorsement_title')
    endorsement_body = request.form.get('endorsement_txt')

    endorsements.save_endorsement_info_to_database(sender, mentor, endorsement_title, endorsement_body)

    return redirect(url_for('mentor_page', linkedin_id=mentor))

# SELF PROFILE PAGES
@app.route('/profile', methods=["GET"])
def self_page():
    if 'linkedin_id' in session:
        ment_data = search.mentor_detail_display(session['linkedin_id'])
        profile_endorsement_hist = endorsements.get_endorsement_info_for_self()
        return render_template('self_profile.html', ment_data=ment_data, profile_endorsement_hist=profile_endorsement_hist)
    return redirect(url_for('login'))

@app.route('/profile', methods=["POST"])
def update_self_page():
    if 'linkedin_id' in session:
        ment_data = search.mentor_detail_display(session['linkedin_id'])
        update_data = tabledef.update_linkedin_user()
        return render_template('self_profile.html', ment_data=ment_data)
    return redirect(url_for('self_page'))

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

# EMAIL FORM Page
@app.route('/email/<linkedin_id>', methods=["GET"])
def email_get(linkedin_id):
    ment_data = search.mentor_detail_display(linkedin_id)
    user_data = search.mentor_detail_display(session['linkedin_id'])
    email_history = email_module.get_email_history_per_mentor(linkedin_id)
    return render_template('email_form.html', ment_data=ment_data, user_data=user_data, email_history=email_history)

@app.route('/email', methods=["POST"])
def email_post():
    sender = session['linkedin_id']
    sender_data= search.mentor_detail_display(sender)
    sender_email = sender_data.email

    mentor = request.form.get('mentor_id')
    mentor_data = search.mentor_detail_display(mentor)
    mentor_email = mentor_data.email

    subject = request.form.get('subject')
    subject_body = request.form.get('message')

    email_module.save_email_info_to_database(sender, mentor, subject, subject_body)
    email_module.send_email(sender_email, mentor_email, subject, subject_body)

    messages = flash('Success! Your message has been sent successfully.')

    return redirect(url_for('email_get', linkedin_id=mentor, messages=messages))

# EMAIL INBOX Page
@app.route('/email_history', methods=["GET"])
def email_history():
    user_data = search.mentor_detail_display(session['linkedin_id'])
    email_history = email_module.get_email_history()
    return render_template('email_history.html', user_data=user_data, email_history=email_history)

@app.route('/email_sent_history', methods=["GET"])
def email_sent_history():
    user_data = search.mentor_detail_display(session['linkedin_id'])
    email_history = email_module.get_sent_email_history_per_sender()
    return render_template('email_sent_history.html', user_data=user_data, email_history=email_history)

@app.route('/email_detail/<email_id>', methods=["GET"])
def email_detail(email_id):
    eid = email_module.get_email_with_id(email_id)
    email_selected = {}
    email_selected["id"]          = eid.id
    email_selected["receiver_id"] = eid.receiver_id
    email_selected["sender_id"]   = eid.sender_id
    email_selected["sent_date"]   = eid.sent_date.strftime("%d/%m/%Y")
    email_selected["subject"]     = eid.subject
    email_selected["text_body"]   = eid.text_body

    email_selected["sender"] = {}
    email_selected["sender"]["first_name"] = eid.sender.first_name
    email_selected["sender"]["last_name"] = eid.sender.last_name

    return json.dumps(email_selected)

@app.route('/delete_email/<int:id>', methods=["GET"])
def delete_email(id):
    if 'linkedin_id' not in session:
        return 'error'
    email_module.delete_email(id)
    return str(id)

@app.route('/about', methods=["GET"])
def about_us():
    return render_template('about_us.html')


   