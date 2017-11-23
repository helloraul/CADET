import string
"""
Comment: [container class]

Class that contains information regarding each student comment (and the
comment itself) For each comment activly store: sentiment, topic_model_id,
instructor_name
"""
class Comment(object):
    sentiment_classifier = ''
    #confidence = 0
    topic_model_id = 0
    comment = ''
    course_comments = ''
    instructor_comments = ''
    additional_comments = ''
    instructor_last_name = ''
    instructor_first_name = ''
    course_program = ''
    course_modality = 0
    course_num_sect_id = ''
    anon_id = 0
    comment_id = 0

    def show(self):
        print('Course: ' + self.course_num_sect_id)
        print('Professor: ' + self.instructor_first_name + ' ' + self.instructor_last_name)
        print('Comment: ' + self.comment)
        print('Sentiment: ' + self.sentiment_classifier)
        if self.course_comments:
            print('Course comment: ' + self.course_comments)
        if self.instructor_comments:
            print('Instructor comment: ' + self.instructor_comments)
        if self.additional_comments:
            print('Additional comment: ' + self.additional_comments)
        print('Comment ID: ' + str(self.comment_id))
 

    def getSentimentClass(self):
        return self.sentiment_classifier

    #def getConfidence(self):
    #    return self.confidence

    def getTopicModelId(self):
        return self.topic_model_id

    def getComment(self):
        return self.comment

    def setSentimentClass(self, sentiment):
        self.sentiment_classifier = sentiment

    #def setConfidence(self, confidence):
    #    self.confidence = confidence

    def setTopicModelId(self, id):
        self.topic_model_id = id

    def setInstructorName(self, name):
        full_name = name.split(' ')
        self.instructor_last_name = full_name[1]
        self.instructor_first_name = full_name[0]

    def getInstructorName(self):
        return (self.instructor_last_name, self.instructor_first_name)

    def setCourse(self, program, modality, num_sec):
        self.course_program = program
        self.course_modality = modality
        self.course_num_sect_id = num_sec

    def getCourse(self):
        return (self.course_program, self.course_modality, self.course_num_sect_id)

    def getCourseCommentDict(self):
        list = [self.sentiment_classifier, self.topic_model_id]
        return {self.comment: list}

    def getInstructorCommentDict(self):
        list = [self.instructorName, self.sentiment_classifier, \
                self.topic_model_id]
        return {self.comment: list}


# Can initialize with just a comment. Or, when reading in from JSON file,
# initialize with a dictionary. dictionaries may or may not have the
# instructor_name commentDict = <comment, [(instructorName), sentiment,
# topic_model_id] > mapping

    def __init__(self, commentDict = None, comment =""):
        #load comment from JSON dictionary

        if commentDict is not None and isinstance(commentDict, dict):
            printable = set(string.printable)
            self.comment = ''.join( filter(lambda x: x in printable, \
                list(commentDict.keys())[0]) )

            if commentDict.get(self.comment) is not None and \
                len(commentDict.get(self.comment)) == 2:
                self.sentiment_classifier = commentDict.get(self.comment)[0]
                self.topic_model_id = commentDict.get(self.comment)[1]
            elif commentDict.get(self.comment) is not None and \
                len(commentDict.get(self.comment)) == 3:
                self.instructorName = commentDict.get(self.comment)[0]
                self.sentiment_classifier = commentDict.get(self.comment)[1]
                self.topic_model_id = commentDict.get(self.comment)[2]
        else:
            self.comment = comment
