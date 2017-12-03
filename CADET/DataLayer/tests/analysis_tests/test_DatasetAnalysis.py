import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)

from cadetapi.controllers.analysis.Comment import Comment as CommentObject
from cadetapi.controllers.analysis.DatasetAnalysis import DatasetAnalysis as Analyzer


db_comments = list()
db_comments.append({'course_num_sect_id': '605.423', 'instructor_last_name': 'Bennett', 'modality': 'in-person', 'additional_comments': 'The campus is in a really convenient location', 'anon_id': 42, 'instructor_comments': 'The instructor did a good job of challenging the students', 'program': 'Engineering', 'course_comments': 'I like this class overall', 'instructor_first_name': 'Joe'})

num_topics = [0, 1, 2]
words_per_topic = [0, 1, 2]
iterations = [0, 1, 2]
dataset_id = [0, 1, 2]



def test_format_comments():
    analyzer = Analyzer(0)
    for index, db_comment in enumerate(db_comments):
        course_comment, instructor_comment = analyzer.formatDbComment(db_comment, index)
        assert course_comment['course_num_sect_id'] == instructor_comment['course_num_sect_id'] == db_comment['course_num_sect_id']
        assert course_comment['instructor_last_name'] == instructor_comment['instructor_last_name'] == db_comment['instructor_last_name']
        assert course_comment['instructor_first_name'] == instructor_comment['instructor_first_name'] == db_comment['instructor_first_name']
        assert course_comment['modality'] == instructor_comment['modality'] == db_comment['modality']
        assert course_comment['anon_id'] == instructor_comment['anon_id'] == db_comment['anon_id']
        assert course_comment['program'] == instructor_comment['program'] == db_comment['program']
        assert course_comment['comment'] == db_comment['course_comments']
        assert instructor_comment['comment'] == db_comment['instructor_comments']
        assert course_comment['sentiment'] == instructor_comment['sentiment'] == ''
        assert course_comment['topic_model_id'] == instructor_comment['topic_model_id'] == 0
        assert course_comment['comment_type'] == 'course'
        assert instructor_comment['comment_type'] == 'instructor'

# def test_get_comment_objects():

def test_init():
    for i in range(0, len(dataset_id)):
        analyzer = Analyzer(dataset_id[i], num_topics = num_topics[i], words_per_topic = words_per_topic[i], iterations = iterations[i])            

        assert analyzer.num_topics == num_topics[i]
        assert analyzer.words_per_topic == words_per_topic[i]
        assert analyzer.iterations == iterations[i]
        assert analyzer.dataset_id == dataset_id[i]
