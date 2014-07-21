from flask_oauthlib.client import OAuth
from flask import Flask, render_template, redirect, jsonify, request, flash, url_for, session
import jinja2
import tabledef
from tabledef import User, MentoreeTopic, Topic
import linkedin
from xml.dom.minidom import parseString
# from Project import app

def search(searchtopics):
	# logic:
	# grabbing it from database and get results page
	# pass results back to main.py to render
	# return render to search results page
	mentor_data = []
	mentor_search_dict = {}
	search_results=tabledef.dbsession.query(tabledef.MentoreeTopic).filter_by(topic_id=searchtopics).all()
	print "!!~~~ SEARCH RESULTS!!~~~"
	print search_results[0].topic_id
	for mentor in search_results:
		ment_data = tabledef.dbsession.query(tabledef.User).filter_by(linkedin_id=mentor.mentor_id).first()
		result_dict = ment_data.__dict__
		mentor_data.append(result_dict)
	# for mentor in search_results:
	# 	# print mentor.mentor_id
	# 	ment_data = tabledef.dbsession.query(tabledef.User).filter_by(linkedin_id=mentor.mentor_id).first()
	# 	mentor_data.append(ment_data)
	# print(dict(zip(mentor.keys(), mentor)))
	return mentor_data