import string

"""
Comment: [container class]

Class that contains information regarding each student comment (and the
comment itself) For each comment activly store: sentiment, topic_model_id,
instructor_name
"""

class Comment():

    anon_id = 0
    comment = ''
    comment_id = 0
    comment_type = ''
    course = ''
    instructor_first_name = ''
    instructor_last_name = ''
    sentiment = ''
    topic_model_id = 0

    def show(self):
        print('Course: ' + self.course)
        print('Instructor: ' + self.instructor_first_name + ' ' + self.instructor_last_name)
        print('Comment type: ' + self.comment_type)
        print('Comment: ' + self.comment)
        print('Sentiment: ' + self.sentiment)
        print('Comment ID: ' + str(self.comment_id))
        
    def getSentiment(self):
        return self.sentiment

    def getCommentId(self):
        return self.comment_id

    def getTopicModelId(self):
        return self.topic_model_id

    def getComment(self):
        return self.comment

    def setSentiment(self, sentiment):
        self.sentiment = sentiment

    def setTopicModelId(self, topic_model_id):
        self.topic_model_id = topic_model_id

    def getInstructor(self):
        return (self.instructor_first_name, self.instructor_last_name)

    def setInstructor(self, first_name, last_name):
        self.instructor_first_name = first_name
        self.instructor_last_name - last_name


    def setCourse(self, program, modality, num_sec):
        return course

    def getCourse(self):
        return (self.course_program, self.course_modality, self.course_num_sect_id)

    def __init__(self, comment = ' ', comment_type = ' ', comment_id = 0):

        self.comment = comment
        self.comment_type = comment_type
        self.comment_id = comment_id

