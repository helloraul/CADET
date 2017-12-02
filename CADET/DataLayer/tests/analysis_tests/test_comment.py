import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)

from cadetapi.controllers.analysis.Comment import Comment as CommentObject

# These are the attributes in the Comment class
comment_keys = ['anon_id', 'comment', 'comment_id', 'comment_type', 'course_modality', 'course_num_sect_id',
        'instructor_first_name', 'instructor_last_name', 'sentiment', 'topic_model_id']

# Test cases
# These need to be fleshed out more
comments = ['', 'a', 'This is a course comment']
instructor_first_names = ['', 'F', 'This is a really long first name']
instructor_last_names = ['', 'L', 'This is a really long last name']
course_num_sect_ids = ['', 22, 'A']
topic_model_ids = ['', 22, 'A']
sentiments = ['', 22, 'pos']
comment_types = ['', 22, 'comment type']
comment_ids = ['', 22, 'A']
anon_ids = ['', 22, 'A']
course_modality = ['', 22, 'A']

comment_dicts = list()
comment_dicts.append({})
comment_dicts.append({'comment':'Hi'})
comment_dicts.append({'Comment':'Hi', 'comment':'bye'})

def test_init():
    comment_object = CommentObject()
    for i in range(0,len(comments)):
        comment_object.__init__(comment = comments[i], comment_type = comment_types[i], comment_id = comment_ids[i])
        assert comment_object.getComment() == comments[i]
        assert comment_object.getCommentType() == comment_types[i]
        assert comment_object.getCommentId() == comment_ids[i]

def test_conversion():
    comment_object = CommentObject()
    for comment_dict in comment_dicts:
        comment_object.convertFromCommentDict(comment_dict)
        # remove keys from test case that are not in the comment_keys
        for key in list(comment_dict.keys()):
            if key not in comment_keys:
                del comment_dict[key]
        # check that the comment_object contains all data in the comment_dict
        assert set(comment_dict.items()).issubset(set(comment_object.convertToCommentDict().items()))
        # check that output contails all comment_keys
        assert all(key in comment_keys for key in comment_object.convertToCommentDict().keys())
        # check that output contains only comment_keys
        assert all(key in comment_object.convertToCommentDict().keys() for key in comment_keys)

def test_getters_setters():
    comment_object = CommentObject()
    for i in range(0, len(comments)):
        comment_object.setComment(comments[i])
        comment_object.setCommentId(comment_ids[i])
        comment_object.setCommentType(comment_types[i])
        comment_object.setCourse(course_num_sect_ids[i])
        comment_object.setInstructor(instructor_first_names[i], instructor_last_names[i])
        comment_object.setModality(course_modality[i])
        comment_object.setSentiment(sentiments[i])
        comment_object.setTopicModelId(topic_model_ids[i])
        
        
        assert comment_object.getComment() == comments[i]
        assert comment_object.getCommentId() == comment_ids[i]
        assert comment_object.getCommentType() == comment_types[i]
        assert comment_object.getCourse() == course_num_sect_ids[i]
        assert comment_object.getInstructor() == (instructor_first_names[i], instructor_last_names[i])
        assert comment_object.getModality() == course_modality[i]
        assert comment_object.getSentiment() == sentiments[i]
        assert comment_object.getTopicModelId() == topic_model_ids[i]

