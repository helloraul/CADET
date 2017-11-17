
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui, QtCore, QtWidgets
import os
"""
TopicModelOptions:
If a non-json file has been loaded, The topicModelOptions Dialog will popup
prompting the user to enter params for the topic modeling algorithm:

numTopics = number of topics to find (default = 5)
numWords = number of words per topic  (defualt =6)
numIteratison = Number of iterations over the text (default =30) (more iterations the more accuratly represented topic model)

An option is also available to edit the list of stop words (words that are excluded from the topic model).
"""
class TopicModelOptions(QtWidgets.QDialog):  
    numTopics_textbox = None
    numWords_textbox = None
    numIterations_textbox = None
	
    numTopics = 5
    numWords = 6
    numIterations = 30
	
    def __init__(self):
	    QtWidgets.QDialog.__init__(self)
		
	    self.setWindowTitle("Topic Model Options")

	    num_topics_label = QtWidgets.QLabel(self)
	    num_topics_label.setText("Number of Topics:")
	    num_topics_label.setAlignment(QtCore.Qt.AlignCenter)
	    num_topics_label.move(25, 10)
		
	    self.numTopics_textbox = QtWidgets.QLineEdit(self)
	    self.numTopics_textbox.setText("5")
	    self.numTopics_textbox.move(25, 30)
	    self.numTopics_textbox.resize(50, 20)
		
	    num_words_label = QtWidgets.QLabel(self)
	    num_words_label.setText("Number of words per topic: ")
	    num_words_label.setAlignment(QtCore.Qt.AlignCenter)
	    num_words_label.move(25, 80)
		
	    self.numWords_textbox = QtWidgets.QLineEdit(self)
	    self.numWords_textbox.setText("6")
	    self.numWords_textbox.move(25, 100)
	    self.numWords_textbox.resize(50, 20)
		
	    num_iterations_label = QtWidgets.QLabel(self)
	    num_iterations_label.setText("Number of Iterations: ")
	    num_iterations_label.setAlignment(QtCore.Qt.AlignCenter)
	    num_iterations_label.move(25, 150)
		
	    self.numIterations_textbox = QtWidgets.QLineEdit(self)
	    self.numIterations_textbox.setText("30")
	    self.numIterations_textbox.setToolTip("Used to perform Latent Dirichlet Allocation statistical model")
	    self.numIterations_textbox.move(25, 170)
	    self.numIterations_textbox.resize(50, 20)
		
	    edit_button = QtWidgets.QPushButton("Edit StopWords", self)
	    edit_button.move(25, 220)
	    edit_button.setToolTip("stop_words are ignored when buiding the topic model")
	    edit_button.clicked.connect(self.openFileInApplication)
	    
	    ok_button = QtWidgets.QPushButton("OK", self)
	    ok_button.move(100, 260)
	    ok_button.clicked.connect(self.okAndClose)

	# open the OS's default text editor
    def openFileInApplication(self):
	    if os.name == 'nt':   #windows os
                
                print("Windows was detected")
                os.system("start" + "../resources/stop_words.txt")
	    else:                 #mac os 
                print("Mac OS was detected")
                os.system("open " + "../resources/stop_words.txt")

			 
    def okAndClose(self):
	    try: 
		    self.numTopics = int( self.numTopics_textbox.text() )
		    self.numWords = int( self.numWords_textbox.text() )
		    self.numIterations = int( self.numIterations_textbox.text() )
		    self.close()
        
	    except ValueError:
		    self.numTopics_textbox.setText("5")
		    self.numWords_textbox.setText("6")		
		    self.numIterations_textbox.setText("30")

    def getNumTopics(self):
	    return self.numTopics
		
    def getNumWords(self):
	    return self.numWords
		
    def getNumIterations(self):
	    return self.numIterations
