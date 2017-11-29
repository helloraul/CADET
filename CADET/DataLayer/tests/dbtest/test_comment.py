# Need to append to the path in order to import the right files
import sys
sys.path.append('cadetapi/')
sys.path.append('cadetapi/controllers/database/')

from DbControl import *

# Test Case for comment stuff
# first I have to create dictionary to hold the comment
MyComment = {}
MyComment['anon_id'] = 42
MyComment['instructor_first_name'] = 'Joe'
MyComment['instructor_last_name'] = 'Bennett'
MyComment['course_program'] = 'Engineering'
MyComment['course_modality'] = 'in-person'
MyComment['course_num_sect_id'] = '605.423'
MyComment['course_comments'] = 'I like this class overall'
MyComment['instructor_comments'] = 'The instructor did a good job of challenging the students'
MyComment['additional_comments'] = 'The campus is in a really convenient location'

NewComment = DbComment()
comm_pk = NewComment.GetId(MyComment)
print('New comment stored as: ', comm_pk)
