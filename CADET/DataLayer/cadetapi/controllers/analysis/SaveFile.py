import json
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui, QtCore, QtWidgets
from Comment import Comment 
from FileIngesterUtil import FileIngesterUtil

"""
PopupSave - opens a dialog box to promt the user for a save file name.
When the user presses 'ok', we loop over the array of FileIngesterUtil objs and save
the information gained from the AnalysisModule (a.k.a save data that otherwise takes very long to compute)

-This alows the user to reload their saved results instantly 

*****Json Files have the folowing outline**********
(first line) = (int) number of semester file saved
---Then for every file saved ----
(newLine):"title:"(title of the semester ex: "Spring2016")
(newLine):"course:"(topic model sentiment histogram dictionary as a string)
(newLine):"course:"(topic model dictionary as a string)
(newLine):"course:"(comment dictionary list-> list of dictionaries with <comment, [sentiment, topicmodel_id]> mapping )
(newLine):"instructor:"(comment dictionary list-> list of dictionaries with <instructor_comment, [sentiment, topicmodel_id]> mapping )
(newLine):"instructor":(instructor sentiment dictionary as string )
(newLine):

"""
class PopupSave(QtWidgets.QWidget):  
    textbox = None
    fileUtilArray = []
    instructorSentimentArray = []
    courseSentimentArray = []
# we needed to make deep copies of instructorSentimentArray & courseSentimentArray. Passing by reference would 
#overwrite pointers. See CommmentAnaylsisApp for where this is done.
    def __init__(self, fileUtilArray = None, instructorSentimentArray=None, courseSentimentArray=None ):
	    QtWidgets.QWidget.__init__(self)
	    self.fileUtilArray = fileUtilArray
	    self.instructorSentimentArray = instructorSentimentArray
	    self.courseSentimentArray = courseSentimentArray
		
	    p = self.palette()
	    p.setColor(self.backgroundRole(), QtCore.Qt.white)
	    self.setPalette(p)
		
	    self.setWindowTitle("Save file name")
		
	    label = QtWidgets.QLabel(self)
	    label.setText("Enter save file name:")
	    label.setAlignment(QtCore.Qt.AlignCenter)
	    label.move(1, 1)
		
	    self.textbox = QtWidgets.QLineEdit(self)
	    self.textbox.move(25, 20)
	    self.textbox.resize(280, 30)
		
	    save_button = QtWidgets.QPushButton("Save", self)
	    save_button.move(20, 60)
	    save_button.clicked.connect(self.createSave)
		
	    cancle_button = QtWidgets.QPushButton("Cancel", self)
	    cancle_button.move(120, 60)
	    cancle_button.clicked.connect(self.closeWindow)
		
	#create a jason file from the local save directory
    def createSave(self):   
	    
	    fileName = "../saves/"+self.textbox.text()+".json"
	    file = open(fileName, 'w')
	    count = 0
	    file.write(str(len(self.fileUtilArray)))  # number of files 
	    file.write("\n")
		
	    for fileUtil in self.fileUtilArray:
		    file.write("title:")
		    file.write( fileUtil.getFileTitle() )
		    #file.write("_")
		    #file.write(str(count))
		    file.write("\n")
		    commentStore = [obj.getCourseCommentDict() for obj in fileUtil.getCommentList()]
		    file.write("course:")
		    json.dump(self.courseSentimentArray[count], file, sort_keys=True)
		    file.write('\n')
		    file.write("course:")
		    json.dump(fileUtil.getTopicModel(), file, sort_keys=True)
		    file.write('\n')
		    file.write("course:")
		    json.dump(commentStore, file)
		    file.write('\n')
			
		    if fileUtil.hasInstructorData:
			    instructorCommentStore = [obj.getInstructorCommentDict() for obj in fileUtil.getInstructorComments()]
			    file.write("instructors:")
			    json.dump(instructorCommentStore, file)
			    file.write('\n')
			    file.write("instructors:")
			    json.dump(self.instructorSentimentArray[count], file, sort_keys=True)
			    file.write('\n')
				
		    file.write('\n')
		    count += 1
	    self.close()
	    
    def closeWindow(self):
	    self.close()
	    
		