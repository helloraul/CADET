
CommentExample1 = {}
CommentExample1['anon_id'] = "42"
CommentExample1['instructor_first_name'] = "Joe"
CommentExample1['intstuctor_last_name'] = "Bennett"
CommentExample1['program'] = "Engineering"
CommentExample1['modality'] = "in-person"
CommentExample1['course_num_sect_id'] = "605.423"
CommentExample1['course_comments'] = "I like this class overall"
CommentExample1['instructor_comments'] = "The instructor did a good job of challenging the students"
CommentExample1['additional_comments'] = "The campus is in a really convenient location"

CommentExample2 = {}
CommentExample2['anon_id'] = "42"
CommentExample2['instructor_first_name'] = "Joel"
CommentExample2['intstuctor_last_name'] = "Coffman"
CommentExample2['program'] = "CyberSecurity"
CommentExample2['modality'] = "in-person"
CommentExample2['course_num_sect_id'] = "605.423"
CommentExample2['course_comments'] = "I do not really like the school very much"
CommentExample2['instructor_comments'] = "The instructor did not assign enough homework"
CommentExample2['additional_comments'] = ""

CommentExample3 = {}
CommentExample3['anon_id'] = "42"
CommentExample3['instructor_first_name'] = "Joel"
CommentExample3['intstuctor_last_name'] = "Coffman"
CommentExample3['program'] = "Engineering"
CommentExample3['modality'] = "in-person"
CommentExample3['course_num_sect_id'] = "605.404"
CommentExample3['course_comments'] = "I like this class overall"
CommentExample3['instructor_comments'] = "The instructor did a good job of challenging the students"
CommentExample3['additional_comments'] = "The campus is in a really convenient location"

CourseExample1 = {}
CourseExample1['course_program'] = "Engineering"
CourseExample1['course_modality'] = "in-person"
CourseExample1['course_num_sect_id'] = "605.404"

CourseExample2 = {}
CourseExample2['course_program'] = "Computer Science"
CourseExample2['course_modality'] = "online"
CourseExample2['course_num_sect_id'] = "605.421"

InstructorExample1 = {}
InstructorExample1['instructor_first_name'] = "Joe"
InstructorExample1['instructor_last_name'] = "Garrison"

InstructorExample2 = {}
InstructorExample2['instructor_first_name'] = "Michael"
InstructorExample2['instructor_last_name'] = "Zelster"

StopwordExample = {}
StopwordExample['word_id'] = "31"
StopwordExample['stop_word'] = "ubiquitous"

MetaExample1 = {}
MetaExample1['document_id_number'] = 57
MetaExample1['user_selected_number_topics'] = 3
MetaExample1['user_selected_numer_iterations'] = 10
MetaExample1['user_selected_words_per_topic'] = 4

class MetaExample2():
    document_id_number = 54
    user_selected_number_topics = 5
    user_selected_number_iterations = 250
    user_selected_words_per_topic = 1

class CommentSentimentExample():
    positive = ['comment1', 'comment2']
    negative = ['negative1', 'negative2']
    neutral = ['neutral3', 'neutral10']

class DatasetExample():
    meta_file_info = MetaExample2()
    raw_file_stats = [CommentExample1, CommentExample2, CommentExample3]

ResultTopicExample = {}
ResultTopicExample['words'] = ['Hello', 'Goodbye', 'bun']
ResultTopicExample['comments'] = CommentSentimentExample()

ResultInstructorExample = {}
ResultInstructorExample['instructor_first'] = \
        InstructorExample1['instructor_first_name']
ResultInstructorExample['instructor_last'] = \
        InstructorExample1['instructor_last_name']
ResultInstructorExample['course_num_sect_id'] = '605.123'
ResultInstructorExample['comments'] = CommentSentimentExample()

class ResultExample():
    result_id = 1000
    meta_file_info = MetaExample1
    results = {}
    results['topic_stats'] = []
    results['topic_stats'].append(ResultTopicExample)
    results['instructor_stats'] = []
    results['instructor_stats'].append(ResultInstructorExample)

    def __str__(self):
        string = '{ "result_id" : %s,' % self.result_id
        string += ' "meta_file_info" : %s,' % self.meta_file_info
        string += ' "results" : { topic_stats : %s,' % self.results['topic_stats']
        string += ' instructor_stats : %s,' % self.results['instructor_stats']
        string += ' } }'
        return string
