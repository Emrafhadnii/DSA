from PyQt5 import QtCore, QtGui, QtWidgets


class Node:
    def __init__(self, name, message = ""):
        self.next = None
        self.message = message
        self.name = name
    def __str__(self):
        return f"{self.name}:{self.message}"

class LinkedList:
    def __init__(self):
        self.head = None

    def add_contact(self, name):
        newnode = Node(name)
        if self.head is None:
            self.head = newnode
        else:
            cr = self.head
            while cr.next:
                cr = cr.next
            cr.next = newnode

    def add_contacts(self):
        self.add_contact('mahdi')
        self.add_contact('afshin')
        self.add_contact('reza')

    def All_contacts(self):
        cr = self.head
        contact = []
        if cr is None:
            return
        else:
            while cr:
                contact.append(str(cr))
                cr = cr.next
        return contact
    
    def message(self, name, message):
        cr = self.head
        while cr:
            if cr.name == name:
                cr.message = message
                break
            cr = cr.next


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(337, 162)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Name = QtWidgets.QComboBox(self.centralwidget)
        self.Name.setGeometry(QtCore.QRect(80, 10, 161, 27))
        self.Name.setObjectName("Name")
        self.Text = QtWidgets.QTextEdit(self.centralwidget)
        self.Text.setGeometry(QtCore.QRect(40, 40, 241, 41))
        self.Text.setObjectName("Text")
        self.Send = QtWidgets.QPushButton(self.centralwidget)
        self.Send.setGeometry(QtCore.QRect(100, 90, 111, 31))
        self.Send.setObjectName("Send")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.linked_list = LinkedList()
        self.linked_list.add_contacts()
        self.Name.addItems(self.linked_list.All_contacts())

        self.Send.clicked.connect(self.send_message)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Send.setText(_translate("MainWindow", "Send Message"))

    def send_message(self):
        self.linked_list.message(self.Name.currentText().split(":")[0],self.Text.toPlainText())
        self.Text.setText("")
        self.Name.clear()
        self.Name.addItems(self.linked_list.All_contacts())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())