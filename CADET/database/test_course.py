from cadet_insert import *

# Test Case for inserting and/or fetching a Course
incrs = DbCourse()
incrsId = incrs.GetId('Computer Science', 3, '605.411')
print('Course ID: ', incrsId)
print('Now Check again')
incrsId = incrs.GetId('Computer Science', 3, '605.411')
print('Course ID: ', incrsId)
