from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine("sqlite:///mentoring.db", echo=False)
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
    age = Column(Integer, nullable = True)
    gender = Column(String(1), nullable = True)
    description = Column(String(501), nullable = True)
    #~~~#
    industry = Column(String(64), nullable = True)
    headline = Column(String(100), nullable = True)
    picture_url = Column(String(200), nullable = True)
    # educations
    educations_start_year = Column(Integer, nullable = True)
    educations_end_year = Column(Integer, nullable = True)
    educations_school_name = Column(String(200), nullable = True)
    educations_field_of_study = Column(String(200), nullable = True)
    educations_degree = Column(String(200), nullable = True)
    # positions
    positions_start_year = Column(Integer, nullable = True)
    positions_end_year = Column(Integer, nullable = True)
    positions_company_name = Column(String(200), nullable = True)
    positions_industry = Column(String(200), nullable = True)
    positions_title = Column(String(200), nullable = True)

    certifications = Column(String(200), nullable = True)
    summary = Column(String(500), nullable=True)
    #make sure the token is the same. person is logged in for the rest of session
    
    def import_linkedin_user(self, data):
        # parsing siteStandardProfileRequest to get authToken
        self.linkedin_id = data.get('id',None)
        self.new_user = True
        token = data.get('siteStandardProfileRequest', None)
        if token != None:
            token_data = token['url']
            start = token_data.find('authToken=')+10
            end = token_data.find('=api', start)
            self.linkedintoken = token_data[start:end]

        self.first_name = data.get('firstName', None)
        self.last_name = data.get('lastName', None)
        self.email = data.get('emailAddress', None)
        self.industry = data.get('industry', None)
        self.headline = data.get('headline',None)

        educations = data.get('educations',None)
        ed_values = educations.get('values',None)
        if ed_values != None:
            for entry in ed_values:
                if 'startDate' in entry:
                    edstartyear = entry['startDate']['year']
                    # print edstartyear
                    self.educations_start_year = edstartyear
                if 'endDate' in entry:
                    edendyear = entry['endDate']['year']
                    # print edendyear
                    self.educations_end_year = edendyear
                if 'schoolName' in entry:
                    schlname = entry['schoolName']
                    # print schlname
                    self.educations_school_name = schlname
                if 'fieldOfStudy' in entry:
                    edfield = entry['fieldOfStudy']
                    # print edfield
                    self.educations_field_of_study = edfield
                if 'degree' in entry:
                    eddegree = entry['degree']
                    # print eddegree
                    self.educations_degree = eddegree

        positions = data.get('positions',None)
        pos_values = positions.get('values',None)
        if pos_values != None:
            for entry in pos_values:
                if 'startDate' in entry:
                    posstartyear = entry['startDate']['year']
                    # print posstartyear
                    self.positions_start_year = posstartyear
                if 'endDate' in entry:
                    posendyear = entry['endDate']['year']
                    # print posendyear
                    self.positions_end_year = posendyear
                if 'title' in entry:
                    postitle = entry['title']
                    # print postitle
                    self.positions_title = postitle
                if 'company' in entry:
                    coname = entry['company']['name']
                    # print coname
                    self.positions_company_name = coname

        cert = data.get('certifications',None)
        if cert != None:
            cert_name = cert['values'][0]['name']
            self.certifications = cert_name

        self.summary = data.get('summary',None)
        self.picture_url = data.get('pictureUrl', None)


class MentoreeTopic(Base):
    __tablename__ = "mentoree_topics"
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'), nullable=True)
    mentor_id = Column(Integer, ForeignKey('users.linkedin_id'), nullable=True)

class Topic(Base):
    __tablename__ = "topics"
    topic_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=True)

def createTable():
    Base.metadata.create_all(engine)

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
