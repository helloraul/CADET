import os, sys, inspect
import multiprocessing
from multiprocessing import Process, Pipe, freeze_support

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)

from cadetapi.controllers.analysis.AnalysisModule import AnalysisModule as Analyzer
from cadetapi.controllers.analysis.Comment import Comment as CommentObject

sentiments  = ['positive', 'negative', 'neutral']
instructor_comment_objects = [
        CommentObject(comment_dict = {'comment':'hello', 'comment_type':'instructor',
            'instructor_first_name':'Who', 'instructor_last_name':'Cares'}),
        CommentObject(comment_dict = {'comment':'goodbye', 'comment_type':'instructor',
            'instructor_first_name':'Who', 'instructor_last_name':'Cares'}) ]

course_comment_objects = [
        CommentObject(comment_dict = {'comment':'hello', 'comment_type':'course'}),
        CommentObject(comment_dict = {'comment':'goodbye', 'comment_type':'course'}) ]

comment_objects = instructor_comment_objects + course_comment_objects

course_comment_text = 'hello ' + 'goodbye '    

def test_separate_comment_types():
    analyzer = Analyzer()
    analyzer.comment_objects = comment_objects
    analyzer.separateCommentTypes()
    assert analyzer.getInstructorComments() == instructor_comment_objects
    assert analyzer.getCourseComments() == course_comment_objects
    assert analyzer.text == course_comment_text

# find a better way to do this
# invalid results would occur if multiple different comments share a comment_id
def test_sentiment_processing():
    analyzer = Analyzer()
    analyzer.courseCommentList = course_comment_objects
    analyzer.instructorCommentList = course_comment_objects

    # create separate thread for analyzing course comments
    if analyzer.courseCommentList is not None:
        analyzer.qList, childPipe = Pipe()
        ctx1 = multiprocessing.get_context('spawn')
        analyzer.sentiment_process = ctx1.Process(target=analyzer.processSentiment, args=(childPipe, analyzer.courseCommentList))
        analyzer.sentiment_process.daemon=True
        analyzer.sentiment_process.start()

    # create separate thread for analyzing instructor comments
    if analyzer.instructorCommentList is not None: 
        analyzer.instructorListPipe, commentPipe= Pipe()  
        ctx2 = multiprocessing.get_context('spawn')
        analyzer.instructor_process = ctx2.Process(target=analyzer.processInstructorComments, args=(commentPipe, analyzer.instructorCommentList))
        analyzer.instructor_process.start()
        
    analyzer.updateAttributes()

    # check if a sentiment is now attached
    for comment_object in analyzer.getCourseComments():
        assert comment_object.getSentiment() in sentiments
    for comment_object in analyzer.getInstructorComments():
        assert comment_object.getSentiment() in sentiments

    # check that number of comments in histogram = number of instructor comments
    instructor_sentiment_histogram = analyzer.getInstructorSentimentHistogram()
    count = 0
    for name in instructor_sentiment_histogram.keys():
        count += instructor_sentiment_histogram.get(name)[0]
        count += instructor_sentiment_histogram.get(name)[1]
        count += instructor_sentiment_histogram.get(name)[2]
    assert count == len(instructor_comment_objects)

def test_topic_model():
    num_topics = 5
    num_words_per_topic = 5
    num_iterations = 5
    analyzer = Analyzer(num_topics = num_topics, words_per_topic=num_words_per_topic, iterations=num_iterations)
    analyzer.courseCommentList = course_comment_objects
    analyzer.text = course_comment_text
    analyzer.processLDAModel()
    assert analyzer.ldamodel.num_topics == num_topics

    # the number of words_per_topic could be lower if there are not enough words in the comments
    assert analyzer.ldamodel.num_terms <= num_words_per_topic

    analyzer.processTopicSentimentHistogram()
    topic_model = analyzer.getTopicModel()
    topic_sentiment_histogram = analyzer.getTopicHistogram() 
    assert len(topic_model) == analyzer.ldamodel.num_topics

    # check that number of comments in histogram = number of course comments
    count = 0
    for i in range(0, len(topic_model)):
        assert len(topic_model[i]) == analyzer.ldamodel.num_terms
        count += topic_sentiment_histogram.get(i)[0]
        count += topic_sentiment_histogram.get(i)[1]
        count += topic_sentiment_histogram.get(i)[2]
    count += topic_sentiment_histogram.get(-1)[0]
    count += topic_sentiment_histogram.get(-1)[1]
    count += topic_sentiment_histogram.get(-1)[2]
    assert count == len(course_comment_objects)

