from cadet_insert import *

# Test Case for comment stuff
# first I have to create a regular comment object
MyComment = OrigCom.Comment() ;
MyComment.anon_id = 42
MyComment.setInstructorName('Joe', 'Bennett')
MyComment.setCourse('Engineering', 3, '605.423')
MyComment.course_comments = 'I like this class overall'
MyComment.instructor_comments = 'The instructor did a good job of challenging the students'
MyComment.additional_comments = 'The campus is in a really convenient location'

NewComment = DbComment()
comm_pk = NewComment.GetId(MyComment)
print('New comment stored as: ', comm_pk)
