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



print('Now fetch by id (3)')
(lname, fname) = instr.GetInstructor(3)
print(lname+', '+fname)
print('Now fetch by id (4)')
(lname, fname) = instr.GetInstructor(4)
(lname, fname) = instr.GetInstructor(4)
(lname, fname) = instr.GetInstructor(4)
print(lname+', '+fname)

print('Fetch something that does not exist')
daname = instr.GetInstructor(42)
if daname is None:
    print('  - That one does not exist')
else:
    print(daname[0]+', '+daname[1])
