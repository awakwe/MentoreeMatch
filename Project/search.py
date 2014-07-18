from flask_oauthlib.client import OAuth
from flask import Flask, render_template, redirect, jsonify, request, flash, url_for, session
import jinja2
from tabledef import User, MentoreeTopic, Topic
import linkedin
from xml.dom.minidom import parseString
# from Project import app

def search():
	# logic:
	# grabbing it from database and get results page
	# pass results back to main.py to render
	# return render to search results page
	# 