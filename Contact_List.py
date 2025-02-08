from PyQt5 import QtCore, QtGui, QtWidgets
from models.Contact import User, session


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(495, 306)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.add = QtWidgets.QPushButton(self.centralwidget)
        self.add.setGeometry(QtCore.QRect(310, 10, 88, 27))
        self.add.setObjectName("add")
        self.delete_2 = QtWidgets.QPushButton(self.centralwidget)
        self.delete_2.setGeometry(QtCore.QRect(220, 10, 88, 27))
        self.delete_2.setObjectName("delete_2")
        self.name = QtWidgets.QTextEdit(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(50, 10, 161, 31))
        self.name.setObjectName("name")
        self.phone = QtWidgets.QTextEdit(self.centralwidget)
        self.phone.setEnabled(True)
        self.phone.setGeometry(QtCore.QRect(50, 50, 161, 31))
        self.phone.setObjectName("phone")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 10, 51, 19))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 50, 51, 20))
        self.label_2.setObjectName("label_2")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(20, 90, 461, 171))
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName("tableView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 495, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.add.clicked.connect(self.add_contact)
        self.delete_2.clicked.connect(self.delete_contact)
        self.name.textChanged.connect(self.search_contact)
        self.phone.textChanged.connect(self.search_contact)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.add.setText(_translate("MainWindow", "Add"))
        self.delete_2.setText(_translate("MainWindow", "Delete"))
        self.label.setText(_translate("MainWindow", "name"))
        self.label_2.setText(_translate("MainWindow", "phone"))

    def add_contact(self):
        if self.phone.toPlainText() and self.name.toPlainText():
            session.add(User(name=self.name.toPlainText(), phone=self.phone.toPlainText()))
            session.commit()
            self.name.setText("")
            self.phone.setText("")
            self.search_contact()
    
    def delete_contact(self):
        if self.name.toPlainText() and self.phone.toPlainText():
            user = session.query(User).filter_by(name=self.name.toPlainText(), phone=self.phone.toPlainText()).first()
            if user:
                session.delete(user)
                session.commit()
                self.name.setText("")
                self.phone.setText("")
                self.search_contact()

    def search_contact(self):
        if self.name.toPlainText() or self.phone.toPlainText():
            view =  session.query(User).filter(User.name.like(f"{self.name.toPlainText()}%"),User.phone.like(f"{self.phone.toPlainText()}%")).all()
        else:
            view = session.query(User).all()
            # self.tableView.setModel(QtGui.QStandardItemModel())
            # return
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(["Name", "Phone"])
        row = []
        for user in view:
            row = [
                QtGui.QStandardItem(user.name),
                QtGui.QStandardItem(user.phone)
            ]
            model.appendRow(row)
        self.tableView.setModel(model)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
