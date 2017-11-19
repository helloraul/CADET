from flask_restplus import Resource, fields

def comment_fields():
    define = {
        'id': fields.Integer,
        'anon_id': fields.Integer,
        'course_id': fields.Integer,
        'instructor_id': fields.Integer,
        'c_com': fields.String,
        'i_com': fields.String,
        'a_com': fields.String,
        'create_date': fields.DateTime(dt_format='rfc822'),
    }
    return define

def course_fields():
    define = {
        'id': fields.Integer,
        'program': fields.String,
        'modality': fields.String,
        'num_sec': fields.String,
    }
    return define

def instructor_fields():
    define = {
        'id': fields.Integer,
        'first_name': fields.String,
        'last_name': fields.String,
    }
    return define

def dataset_fields():
    define = {
        'id': fields.Integer,
        'create_date': fields.DateTime(dt_format='rfc822'),
    }
    return define

def result_fields():
    define = {
        'id': fields.Integer,
        'dataset_id': fields.Integer,
        'topic_cnt': fields.Integer,
        'word_cnt': fields.Integer,
        'stop_words': fields.String,
        'iterations': fields.Integer,
        'create_date': fields.DateTime(dt_format='rfc822'),
    }
    return define


