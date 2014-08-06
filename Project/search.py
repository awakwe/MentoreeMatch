from flask_oauthlib.client import OAuth
from flask import Flask, render_template, redirect, jsonify, request, flash, url_for, session
import jinja2
import tabledef
from tabledef import User, MentoreeTopic, Topic
import linkedin
from xml.dom.minidom import parseString
import pdb
# from Project import app

def search(searchtopics):
	search_results=tabledef.dbsession.query(tabledef.MentoreeTopic).filter_by(topic_id=searchtopics).all()
	return search_results

def search_topic_display(searchtopics):
	search_results=tabledef.dbsession.query(tabledef.MentoreeTopic).filter_by(topic_id=searchtopics).all()
	search_topic = tabledef.dbsession.query(tabledef.Topic).filter_by(topic_id=search_results[0].topic_id).first()

	search_topic_title = search_topic.title
	print search_topic_title
	return search_topic_title

def mentor_detail_display(linkedin_id):
	# pdb.set_trace()
	ment_data = tabledef.dbsession.query(tabledef.User).filter_by(linkedin_id=linkedin_id).first()
	# print "!!~~~~~~~~~~~ment_data.positions[0].positions_title~~~~~~~~~~~~~~~~~~~~~~!!"
	# print ment_data.positions[0].positions_title
	# ment_data.positions.positions_title
	return ment_data

def mentor_personal_topics(linkedin_id):
	# pdb.set_trace()
	ment_pers_topics = tabledef.dbsession.query(tabledef.MentoreeTopic).filter_by(mentor_id=linkedin_id).all()
	# for topics in ment_pers_topics:
		# print "((((((~~~~~~~~~~~topics.topic_id~~~~~~~~~~~~~~~~~~~~~~))"
		# print topics.topic_id

	return ment_pers_topics
