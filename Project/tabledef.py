from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker, scoped_session
import pdb
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///mentoring.db")
engine = create_engine(DATABASE_URL, echo=True)
dbsession = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = dbsession.query_property()


### Class declarations
class User(Base):
    __tablename__ = "users"

    # use linkedin ID, therefore never duplicating a user
    linkedin_id = Column(String(50), primary_key = True)
    linkedintoken = Column(String(50), nullable = True)
    new_user = Column(Boolean, nullable = True)
    first_name = Column(String(64), nullable = True)
    last_name = Column(String(64), nullable = True)
    email = Column(String(255), nullable = True)
    #~~~# Data From Additional Info Page
    mentor = Column (Boolean, nullable = True)
    age = Column(String(50), nullable = True)
    gender = Column(String(50), nullable = True)
    description = Column(String(1000), nullable = True)
    #~~~#
    industry = Column(String(64), nullable = True)
    headline = Column(String(100), nullable = True)
    picture_url = Column(String(200), nullable = True)
    certifications = Column(String(200), nullable = True)
    summary = Column(String(500), nullable=True)

    educations = relationship("Education")
    positions = relationship("Position")
    
def import_linkedin_user(data):
    user = User();
    # parsing siteStandardProfileRequest to get authToken
    user.linkedin_id = data.get('id',None)
    user.new_user = True
    token = data.get('siteStandardProfileRequest', None)
    if token != None:
        token_data = token['url']
        start = token_data.find('authToken=')+10
        end = token_data.find('=api', start)
        user.linkedintoken = token_data[start:end]

    user.first_name = data.get('firstName', None)
    user.last_name = data.get('lastName', None)
    user.email = data.get('emailAddress', None)
    user.industry = data.get('industry', None)
    user.headline = data.get('headline',None)

    
    educations = data.get('educations',None)
    education_models = []
    # pdb.set_trace()
    ed_values = educations.get('values',None)
    if ed_values != None:
        for entry in ed_values:
            education = Education()
            education.linkedin_id = user.linkedin_id
            if 'startDate' in entry:
                edstartyear = entry['startDate']['year']
                # print edstartyear
                education.educations_start_year = edstartyear
            if 'endDate' in entry:
                edendyear = entry['endDate']['year']
                # print edendyear
                education.educations_end_year = edendyear
            if 'schoolName' in entry:
                schlname = entry['schoolName']
                # print schlname
                education.educations_school_name = schlname
            if 'fieldOfStudy' in entry:
                edfield = entry['fieldOfStudy']
                # print edfield
                education.educations_field_of_study = edfield
            if 'degree' in entry:
                eddegree = entry['degree']
                # print eddegree
                education.educations_degree = eddegree
            education_models.append(education)

    positions = data.get('positions',None)
    position_models = []
    pos_values = positions.get('values',None)
    if pos_values != None:
        for entry in pos_values:
            position = Position()
            position.linkedin_id = user.linkedin_id
            if 'startDate' in entry:
                posstartyear = entry['startDate']['year']
                # print posstartyear
                position.positions_start_year = posstartyear
            if 'endDate' in entry:
                posendyear = entry['endDate']['year']
                # print posendyear
                position.positions_end_year = posendyear
            if 'title' in entry:
                postitle = entry['title']
                # print postitle
                position.positions_title = postitle
            if 'company' in entry:
                co_entry = entry['company']
                if 'name' in co_entry:
                    print "~~~~~~~~~~~~~~~~~~~~~~ company name"
                    print entry
                    print entry['company']
                    coname = entry['company']['name']
                    print coname
                    position.positions_company_name = coname
            position_models.append(position)

    cert = data.get('certifications',None)
    if cert != None:
        cert_name = cert['values'][0]['name']
        user.certifications = cert_name

    mentor_topics = MentoreeTopic()
    mentor_topics.linkedin_id = user.linkedin_id

    user.summary = data.get('summary',None)
    user.picture_url = data.get('pictureUrl', None)

    current_user_id = user.linkedin_id
    # print "~~!!^_^!!~~"
    existing_user = dbsession.query(User).filter_by(linkedin_id = current_user_id).first()
    if existing_user == None:
        dbsession.add(user)
        dbsession.add(mentor_topics)

        for model in education_models:
            # print "model"
            # print model
            dbsession.add(model)

        for models in position_models:
            dbsession.add(models)

        dbsession.commit()

    return user

class Education(Base):
    __tablename__="educations"
    id = Column(Integer, primary_key=True)
    linkedin_id = Column(String(50), ForeignKey('users.linkedin_id'), nullable = True)
    # educations
    educations_start_year = Column(Integer, nullable = True)
    educations_end_year = Column(Integer, nullable = True)
    educations_school_name = Column(String(200), nullable = True)
    educations_field_of_study = Column(String(200), nullable = True)
    educations_degree = Column(String(200), nullable = True)

    # ment_user = relationship("User", backref=backref("educations", order_by=id))

class Position(Base):
    __tablename__="positions"
    id = Column(Integer, primary_key=True)
    linkedin_id = Column(String(50), ForeignKey('users.linkedin_id'), nullable = True)
    positions_start_year = Column(Integer, nullable = True)
    positions_end_year = Column(Integer, nullable = True)
    positions_company_name = Column(String(200), nullable = True)
    positions_industry = Column(String(200), nullable = True)
    positions_title = Column(String(200), nullable = True)

    # ment_user = relationship("User", backref=backref("positions", order_by=id))

class MentoreeTopic(Base):
    __tablename__ = "mentoree_topics"
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'), nullable=True)
    mentor_id = Column(String(50), ForeignKey('users.linkedin_id'), nullable=True)

    ment_user = relationship("User", backref=backref("mentoree_topics", order_by=id))

class Topic(Base):
    __tablename__ = "topics"
    topic_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=True)

# class Endorsement(Base):
#     __tablename__ = "endorsements"
#     id = Column(Integer, primary_key=True)
#     sender_id = Column(Integer, ForeignKey('users.linkedin_id'), nullable = False)
#     receiver_id = Column(Integer, ForeignKey('users.linkedin_id'), nullable = False)
#     title = Column(String(100), nullable=True)
#     endorsements_text = Column(String(500), nullable=True)

#     ment_user = relationship("User", backref=backref("endorsements", order_by=id))

def createTable():
    Base.metadata.create_all(engine)

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
