# Need to append to the path in order to import the right files
import sys
sys.path.append('cadetapi/')
sys.path.append('cadetapi/controllers/database/')

from cadet_insert import *

# Test Case for inserting and/or fetching an instructor
instr = DbInstructor()
print('Check for an instructor')
instrId = instr.GetId('Some', 'Newguy')
instrId = instr.GetId('Some', 'Newguy')
instrId = instr.GetId('Some', 'Newguy')
print('Instructor ID: ', instrId)
print('Now Check a different one')
instrId = instr.GetId('Mark', 'Sutton')
print('Instructor ID: ', instrId)



print('Now fetch by id (1)')
(lname, fname) = instr.GetInstructor(1)
print(lname+', '+fname)
print('Now fetch by id (2)')
(lname, fname) = instr.GetInstructor(2)
(lname, fname) = instr.GetInstructor(2)
(lname, fname) = instr.GetInstructor(2)
print(lname+', '+fname)

print('Fetch something that does not exist')
daname = instr.GetInstructor(42)
if daname is None:
    print('  - That one does not exist')
else:
    print(daname[0]+', '+daname[1])
