# from flask import Flask, render_template, redirect, request, flash, url_for, session
# import jinja2
# import tabledef
# from tabledef import Users, MentorCareer, MentorSkills
# from xml.dom.minidom import parseString
# import os
# import urllib

# app = Flask(__name__)
# app.secret_key = "topsecretkey"
# app.jinja_env.undefined = jinja2.StrictUndefined

# @app.route("/")
# def index():
#     print "hello"
#     return "hello"

# @app.route("/login", methods=["GET"])
# def get_userlogin():
#     error = None
#     f = urllib.urlopen("http://127.0.0.1:5000/login")
#     print "!~~~~!~~~~!"
#     print f.read()
#     # url = os.environ['HTTP_HOST']
#     # xmlDoc = parseString(url)
#     # print xmlDoc
#     # linkedin_auth = {}
#     return render_template("login.html", error = error)

# @app.route("/login", methods=["POST"])
# def login_user():
#     found_user = tabledef.dbsession.query(User).filter_by(email=request.form['email']).first()
#     print "found user", found_user
#     error = None
#     if found_user:
#         print "User found"
#         session['user'] = found_user.id
#         return redirect("/")
#     else:
#         print "User not found"
#         #flash('Invalid username/password.')
#         error = "Invalid Username"
#         return render_template('login.html', error = error)
#     # return redirect("/")

# @app.route("/create_newuser", methods=["GET"])
# def get_newuser():
#     return render_template("newuser.html")

# @app.route("/create_newuser", methods=["POST"])
# def create_newuser():
#     # print "SESSION", tabledef.dbsession
#     user_exists = tabledef.dbsession.query(User).filter_by(email=request.form['email']).first()
#     print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
#     print "USER EXISTS", user_exists
#     if user_exists != None:
#         flash(" User already exists. Please login")
#         return redirect("/create_newuser")
#     else:     
#         user = User(email=request.form['email'], password= request.form['password'], age=request.form['age'], sex=request.form['sex'], occupation=request.form['occupation'], zipcode=request.form['zipcode'])
#         tabledef.dbsession.add(user)
#         tabledef.dbsession.commit()
#         flash("Successfully added new user!")
#         return redirect("/")


# if __name__ == "__main__":
#     app.run(debug = True)