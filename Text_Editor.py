from PyQt5 import QtCore, QtGui, QtWidgets



"""          Stack and Node classes          """

class Node:
    def __init__(self,data):
        self.data = data
        self.next = None
class Stack:
    def __init__(self):
        self.top = None
    def datatop(self):
        if self.top is not None:
            return self.top.data
        else:
            return "-1"
    def push(self,data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
    def pop(self):
        if self.top is None:
            return "-1"
        else:
            temp_node = self.top
            topdata = self.top.data
            self.top = self.top.next
            del(temp_node)
            return topdata



"""          Gui_Apllication          """

class textEdit(QtWidgets.QTextEdit):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        self.backspace_timer = QtCore.QTimer(self)
        self.backspace_timer.setSingleShot(True)
        self.backspace_timer.timeout.connect(self.pobt)
    
    def pobt(self):
        self.main_window.Ustack.push(self.toPlainText())
    
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key.Key_Backspace:
            if not self.backspace_timer.isActive():
                self.main_window.Ustack.push(self.toPlainText())
            self.backspace_timer.start(300)
            super().keyPressEvent(e)
        else:
            self.backspace_timer.stop()
            super().keyPressEvent(e)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(359, 186)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = textEdit(parent=self.centralwidget,main_window=self)
        self.textEdit.setGeometry(QtCore.QRect(10, 20, 341, 91))
        self.textEdit.setObjectName("textEdit")
        self.Undo_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Undo_btn.setGeometry(QtCore.QRect(60, 120, 93, 31))
        self.Undo_btn.setMouseTracking(False)
        self.Undo_btn.setObjectName("Undo_btn")
        self.Redo_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Redo_btn.setGeometry(QtCore.QRect(200, 120, 93, 31))
        self.Redo_btn.setMouseTracking(False)
        self.Redo_btn.setObjectName("Redo_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Text Editor"))
        self.Undo_btn.setText(_translate("MainWindow", "Undo"))
        self.Redo_btn.setText(_translate("MainWindow", "Redo"))
        self.Ustack = Stack()
        self.Ustack.push("")
        self.Rstack = Stack()
        self.Ustack.push("")
        self.Undo_btn.clicked.connect(self.Undo)
        self.Redo_btn.clicked.connect(self.Redo)
    
    """          Undo and Redo functions          """

    def Undo(self):
        if self.Ustack.top is not None:
            if self.Ustack.datatop() == "":
                self.Rstack.push(self.textEdit.toPlainText())
                Ustr = self.Ustack.pop()
                self.textEdit.setText(Ustr)
            else:
                Ustr = self.Ustack.pop()
                self.Rstack.push(Ustr)
                self.textEdit.setText(Ustr)
        else:
            self.Ustack.push("")
        self.textEdit.setFocus()
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.setFocus()
    def Redo(self):
        if self.Rstack.top is not None:
            Rstr = self.Rstack.pop()
            self.Ustack.push(Rstr)
            self.textEdit.setText(Rstr)
        else:
            self.Rstack.push("")
        self.textEdit.setFocus()
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.setFocus()
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())