""" This file defines the models used when referencing the SQLAlchemy
    database. Each model (class) below should define a table within the
    database and how the tables reference each other.
    More information on how to define these SQLAlchemy models can be found at:
    http://flask-sqlalchemy.pocoo.org/2.3/models/
    http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/
"""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Base = db.make_declarative_base(db.Model)

class Instructor(Base):
    __tablename__ = 'instructors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

class Course(Base):
    __tablename__ = 'courses'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(2))
    program = db.Column(db.Integer)
    course = db.Column(db.Integer)
    section = db.Column(db.Integer)
    semester = db.Column(db.String(4))

class Comment(Base):
    __tablename__ = 'comments'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    anon_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    icom = db.Column(db.Boolean) # True/False = Instructor/Course Comment
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    course = db.relationship(Course)
    instructor = db.relationship(Instructor)

class Stop_Word(Base):
    __tablename__ = 'stop_words'
    id = db.Column(db.Integer, primary_key=True)
    stop_word = db.Column(db.String(50), unique=True)

class Dataset(Base):
    __tablename__ = 'datasets'
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Comment_Dataset(Base):
    __tablename__ = 'com_dat'
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'))
    comment = db.relationship(Comment)
    dataset = db.relationship(Dataset)

class Result_Cache(Base):
    __tablename__ = 'results_cache'
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'))
    topic_cnt = db.Column(db.Integer)
    word_cnt = db.Column(db.Integer)
    stop_words = db.Column(db.String(1000))
    iterations = db.Column(db.Integer)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    #query = Column(String(1000), unique=True)
    #result = Column(Text)

class Result_Topic(Base):
    __tablename__ = 'result_cache_topics'
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('results_cache.id'))
    topic = db.Column(db.String(255))
    result = db.relationship(Result_Cache)

class Result_Detail(Base):
    __tablename__ = 'result_cache_comments'
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('results_cache.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    sentiment = db.Column(db.Integer) #1,2,3 = neg, neut, pos
    topic_id = db.Column(db.Integer, db.ForeignKey('result_cache_topics.id'))
    result = db.relationship(Result_Cache)
    comment = db.relationship(Comment)
    topic = db.relationship(Result_Topic)
