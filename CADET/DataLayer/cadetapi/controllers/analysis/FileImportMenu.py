
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui, QtCore, QtWidgets
import os.path
"""
FIleImportMenu:
Called and displayed from CommentAnalysisApp.py. It prompts the User to import a file.
Gives options to add remove mulitple files (each file representing one semester's survey data)

-Adding and removing files requires that corresponding browse buttons and removeButtons are remved as well from the display

-Dialog displays a list of currently selected files

"""
class FileImportMenu(QtWidgets.QDialog):  

    fileNames = []
    fileLabels = []
    browseButtons = []
    removeButtons = []
    numFiles = -1
    grid = QtWidgets.QGridLayout()
    def __init__(self):
	    QtWidgets.QDialog.__init__(self)
	    
	    self.setGeometry(QtCore.QRect( 100, 100, 300, 200 ) )
	    p = self.palette() #set background color white 
	    p.setColor(self.backgroundRole(), QtCore.Qt.white)
	    self.setPalette(p)
		
	    frame = QtWidgets.QFrame(self)
	    frame.resize(300, 100)
	    frame.setLayout(self.grid)
	    
	    scroll = QtWidgets.QScrollArea()
	    scroll.setWidgetResizable(True)
	    scroll.setWidget(frame)
	    
	    self.setWindowTitle("Browse for File")

	    title_label = QtWidgets.QLabel(self)
	    title_label.setText("Browse for file(s) ")
	    title_label.setAlignment(QtCore.Qt.AlignCenter)
	     

	    add_button = QtWidgets.QPushButton("add (+)", self)
	    add_button.setToolTip("Add another file")
	    add_button.move(25,100)
	    add_button.clicked.connect(self.addAnotherFile)

	    ok_button = QtWidgets.QPushButton("OK", self)	    
	    ok_button.clicked.connect(self.okAndClose)
		
	    vLayout = QtWidgets.QVBoxLayout(self)
	    vLayout.addWidget(title_label)
	    vLayout.addWidget(scroll)
	    vLayout.addWidget(add_button)
	    vLayout.addWidget(ok_button)
	    self.setLayout(vLayout)
	    
	    self.addAnotherFile()
	    
	
    def openFile(self):
	    sending_button = self.sender()
		
	    fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', directory="../saves/")
	    fileName_str = fileName[0]
	    file = fileName_str.split('/')
		
	    self.fileNames.append(fileName_str)
	    self.fileLabels.append(QtWidgets.QLabel(self))
	    try:
		    self.fileLabels[int(str(sending_button.objectName()))].setText("../"+file[-1])
	    except ValueError:
		    self.fileLabels[self.numFiles].setText("../"+file[-1]) 
	    
	# addAnotherFile()	
    # adds buttons and labels to the layout and call self.openFile() to promt the user
    def addAnotherFile(self): # add file to list
        
	    self.numFiles += 1
	    self.fileLabels.append(QtWidgets.QLabel(self))
	    self.fileLabels[self.numFiles].resize(20, 20)
	    self.grid.addWidget(self.fileLabels[self.numFiles], (3+len(self.browseButtons)), 2)
		
	    self.browseButtons.append(QtWidgets.QPushButton("Browse", self))
	    self.browseButtons[self.numFiles].clicked.connect(self.openFile)
	    self.browseButtons[self.numFiles].setObjectName(str(self.numFiles))
	    self.browseButtons[self.numFiles].setFixedSize(50, 20)
		
	    self.removeButtons.append(QtWidgets.QPushButton("X", self))
	    self.removeButtons[self.numFiles].clicked.connect(self.removeFile)
	    self.removeButtons[self.numFiles].setObjectName(str(self.numFiles))
	    self.removeButtons[self.numFiles].setFixedSize(20, 20)
		
	    self.grid.addWidget(self.removeButtons[self.numFiles], (2+len(self.browseButtons)), 0)
	    self.grid.addWidget(self.browseButtons[self.numFiles], (2+len(self.browseButtons)), 1)
	    
	    self.openFile()

    def removeFile(self): # remove file from list
	    sending_button = self.sender()
	
	    remove_index = int(str(sending_button.objectName())) 
	    self.fileNames.remove(self.fileNames[remove_index])
	    for i in range(0, len(self.browseButtons)):
		    self.grid.removeWidget(self.fileLabels[i])
		    self.grid.removeWidget(self.browseButtons[i])
		    self.grid.removeWidget(self.removeButtons[i])
		    self.fileLabels[i].setParent(None)
		    self.browseButtons[i].setParent(None)
		    self.removeButtons[i].setParent(None)

	    self.fileLabels.remove(self.fileLabels[remove_index])
	    self.browseButtons.remove(self.browseButtons[remove_index])
	    self.removeButtons.remove(self.removeButtons[remove_index])
	    
	    for i in range(0, len(self.browseButtons)):
		    self.fileLabels[i].setObjectName(str(i))
		    self.browseButtons[i].setObjectName(str(i))
		    self.removeButtons[i].setObjectName(str(i))
		    self.fileLabels[i].setParent(self)
		    self.browseButtons[i].setParent(self)
		    self.removeButtons[i].setParent(self)
		    self.grid.addWidget(self.removeButtons[i], (2+i), 0)
		    self.grid.addWidget(self.browseButtons[i], (2+i), 1)
		    self.grid.addWidget(self.fileLabels[i], (2+i), 2)
			
	    self.numFiles -= 1
		
    cleanExit = False
    def closeEvent(self, event):
	    if self.cleanExit:
		    event.accept()
	    else:
		    self.fileNames.clear()
		    event.accept()
        
    def getFileNames(self): #clear out any bad files and return
	    finalList = []
	    for file in self.fileNames:
		    if os.path.isfile(file):
			    finalList.append(file)

	    return finalList

    def okAndClose(self):
	    self.cleanExit = True
	    self.close()

	# clear the Dialog box, so when we reopen, it is cleared out
    def clearAll(self):
	    for i in range(0, len(self.browseButtons)):
		    self.grid.removeWidget(self.fileLabels[i])
		    self.grid.removeWidget(self.browseButtons[i])
		    self.grid.removeWidget(self.removeButtons[i])
		    self.fileLabels[i].setParent(None)
		    self.browseButtons[i].setParent(None)
		    self.removeButtons[i].setParent(None)
	    self.fileLabels.clear()
	    self.browseButtons.clear()
	    self.removeButtons.clear()
	    self.fileNames.clear()
	    self.numFiles = -1
