from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui, QtCore, QtWidgets

"""
Dialog box that diplays given input string (used for displaying sturdent comments)

press OK or exit-button to close window

"""


class CommentDialog(QDialog):
    
    def __init__(self, parent = None, comment=""):
	    super(CommentDialog, self).__init__(parent)

	    layout = QtWidgets.QVBoxLayout(self)
	    frameLayout = QtWidgets.QVBoxLayout()
	    
	    frame = QtWidgets.QFrame(self)
	    frame.setLayout(frameLayout)
		
	    scroll = QtWidgets.QScrollArea()
	    scroll.setWidgetResizable(True)
	    scroll.setWidget(frame)
		
		
	    commentLabel = QtWidgets.QLabel(self)
	    commentLabel.setWordWrap(True)
	    commentLabel.setText(comment)
	    frameLayout.addWidget(commentLabel)
		
	    layout.addWidget(scroll)
        # OK and Cancel buttons
	    buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok,QtCore.Qt.Horizontal, self)
	    buttons.accepted.connect(self.accept)
	    buttons.rejected.connect(self.reject)
	    layout.addWidget(buttons)
		
	    self.setFixedSize(600, 400)

