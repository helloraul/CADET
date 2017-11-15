import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, \
                       String, Text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()
 
# Create an engine that stores data in the local directory's
# cadet_lite.db file.
def cadEngine():
    return create_engine('sqlite:///cadet_lite.db')
    #return create_engine('mysql://cadet:cadet@localhost/cadet')

class Instructor(Base):
    __tablename__ = 'instructors'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))

class Course(Base):
    __tablename__ = 'courses'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    program = Column(String(20))
    modality = Column(Integer)
    num_sec = Column(String(10))

class Comment(Base):
    __tablename__ = 'comments'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    anon_id = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'))
    instructor_id = Column(Integer, ForeignKey('instructors.id'))
    #icom = Column(Boolean)
    c_com = Column(Text) # Course Comment
    i_com = Column(Text) # Instructor Comment
    a_com = Column(Text) # Additional Comment
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    course = relationship(Course)
    instructor = relationship(Instructor)
 
class Stop_Word(Base):
    __tablename__ = 'stop_words'
    id = Column(Integer, primary_key=True)
    stop_word = Column(String(50), unique=True)
 
class Dataset(Base):
    __tablename__ = 'datasets'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)

class Comment_Dataset(Base):
    __tablename__ = 'com_dat'
    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey('comments.id'))
    dataset_id = Column(Integer, ForeignKey('datasets.id'))
    comment = relationship(Comment)
    dataset = relationship(Dataset)

class Result_Cache(Base):
    __tablename__ = 'results_cache'
    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey('datasets.id'))
    topic_cnt = Column(Integer)
    word_cnt = Column(Integer)
    stop_words = Column(String(1000))
    iterations = Column(Integer)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    #query = Column(String(1000), unique=True)
    #result = Column(Text)

class Result_Topic(Base):
    __tablename__ = 'result_cache_topics'
    id = Column(Integer, primary_key=True)
    result_id = Column(Integer, ForeignKey('results_cache.id'))
    topic = Column(String(255))
    result = relationship(Result_Cache)

class Result_Detail(Base):
    __tablename__ = 'result_cache_comments'
    id = Column(Integer, primary_key=True)
    result_id = Column(Integer, ForeignKey('results_cache.id'))
    comment_id = Column(Integer, ForeignKey('comments.id'))
    sentiment = Column(Integer) #1,2,3 = neg, neut, pos
    result = relationship(Result_Cache)
    comment = relationship(Comment)

class Topic_Word(Base):
    __tablename__ = 'topic_words'
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('result_cache_topics.id'))
    word = Column(String(255))
    topic = relationship(Result_Topic)

def dbsession():
    engine = cadEngine()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(cadEngine())
