# Need to append to the path in order to import the right files
import sys
sys.path.append('cadetapi/')
sys.path.append('cadetapi/controllers/database/')

from DbControl import *

# Test Case for inserting and/or fetching a Course
incrs = DbCourse()
incrsId = incrs.GetId('Computer Science', 'online', '605.411')
print('Course ID: ', incrsId)
print('Now Check again')
incrsId = incrs.GetId('Computer Science', 'online', '605.411')
print('Course ID: ', incrsId)
