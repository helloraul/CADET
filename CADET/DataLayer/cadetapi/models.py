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
"""
def CadEngine():
    return db.create_engine('sqlite:///cadet_lite.db')
    #return db.create_engine('mysql://cadet:cadet@localhost/cadet')
"""
class Instructor(Base):
    # Here we define columns for the 'instructors' table
    # Notice that each column is also a normal Python instance attribute.
    __tablename__ = 'instructors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

class Course(Base):
    # Define columns for the 'courses' table
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(20))
    modality = db.Column(db.String(50))
    num_sec = db.Column(db.String(10))

class Comment(Base):
    # Define columns and relationships for the 'comments' table
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    anon_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    c_com = db.Column(db.Text) # Course Comment
    i_com = db.Column(db.Text) # Instructor Comment
    a_com = db.Column(db.Text) # Additional Comment
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    course = db.relationship(Course)
    instructor = db.relationship(Instructor)

class Stopword(Base):
    # Define columns for the 'stop_words' table
    __tablename__ = 'stop_words'
    id = db.Column(db.Integer, primary_key=True)
    stop_word = db.Column(db.String(50), unique=True)

class DataSet(Base):
    # Define columns for the 'datasets' table
    __tablename__ = 'datasets'
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class CommentDataSet(Base):
    # Define columns and relationships for the 'com_dat' table
    # Table maintains the many-to-many relationship for comments and datasets
    __tablename__ = 'com_dat'
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'))
    comment = db.relationship(Comment)
    dataset = db.relationship(DataSet)

class ResultSet(Base):
    # Define columns for the 'results' table
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'))
    topic_cnt = db.Column(db.Integer) # number of topics
    word_cnt = db.Column(db.Integer)  # words per topic
    stop_words = db.Column(db.String(1000)) # concatenated list of stop-words
    iterations = db.Column(db.Integer) # number of iterations
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class ResultTopic(Base):
    __tablename__ = 'result_topics'
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('results.id'))
    result = db.relationship(ResultSet)

class TopicWord(Base):
    __tablename__ = 'topic_words'
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('result_topics.id'))
    word = db.Column(db.String(255))
    topic = db.relationship(ResultTopic)

class ResultCourseComment(Base):
    __tablename__ = 'result_course_comments'
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('result_topics.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    course_com_sent = db.Column(db.String(8)) # positive, negative, neutral
    topic = db.relationship(ResultTopic)
    comment = db.relationship(Comment)

class ResultInstructorComment(Base):
    __tablename__ = 'result_instructor_comments'
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('results.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    instr_com_sent = db.Column(db.String(8)) # positive, negative, neutral
    result = db.relationship(ResultSet)
    comment = db.relationship(Comment)

def DbSession():
    return db.session
