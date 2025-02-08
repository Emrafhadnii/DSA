from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd

class Node:
    def __init__(self,char=None,freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    def __lt__(self, other):
        return self.freq < other.freq
    

class minheap:
    def __init__(self):
        self.heap = []
    def insert(self,node):
        self.heap.append(node)
        self.sortheap(len(self.heap) - 1)
    
    def sortheap(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[index].freq < self.heap[parent].freq:
                self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
                index = parent
            else:
                break
    def removemin(self):
        if not self.heap:
            return None
        min_node = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.resortheap(0)
        return min_node
    
    def resortheap(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < len(self.heap) and self.heap[left].freq < self.heap[smallest].freq:
            smallest = left
        if right < len(self.heap) and self.heap[right].freq < self.heap[smallest].freq:
            smallest = right
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self.resortheap(smallest)
    
    def __getitem__(self,index):
        return self.heap[index]
    def __iter__(self):
        return iter(self.heap)
    def __len__(self):
        return len(self.heap)


class huffmantree:
    def __init__(self):
        self.root = None
    def create_tree(self,heap:minheap):
        if len(heap) == 0:
            return
        while len(heap) > 1:
            left = heap.removemin()
            right = heap.removemin()
            parent = Node(None, left.freq + right.freq)
            parent.left = left
            parent.right = right
            heap.insert(parent)
        if len(heap) == 1:
            self.root = heap[0]

            
class huffmanalgo:
    def __init__(self,usertext:QtWidgets.QPlainTextEdit, compresedtetx:QtWidgets.QPlainTextEdit):
        self.usertext = usertext
        self.comtext = compresedtetx
        self.tree = None
    
    def gen_code(self,node:Node,bindict:dict,bincode = ""):
        if node is not None:
            if node.char is not None:
                bindict[node.char] = bincode
            self.gen_code(node.left,bindict,bincode+"0")
            self.gen_code(node.right,bindict,bincode+"1")

    
    def Encoder(self):
        countdict = pd.Series(list(self.usertext.toPlainText())).value_counts().to_dict()
        freq = dict(sorted(countdict.items(),key=lambda item : item[1]))
        heap = minheap()
        for k,i in freq.items():
            heap.insert(Node(k,i))
        tree = huffmantree()
        tree.create_tree(heap)
        self.tree = tree
        bindict = {}
        self.gen_code(tree.root,bindict)
        binary_text = ""
        for ch in self.usertext.toPlainText():
            binary_text += bindict[ch]
        self.comtext.setPlainText(binary_text)
        self.usertext.setPlainText("")

        
    def Decoder(self):
        compressed_text = self.comtext.toPlainText()
        usertext = []
        node = self.tree.root
        for char in compressed_text:
            if char == "0":
                node = node.left
            else:
                node = node.right
            if node.char is not None:
                usertext.append(node.char)
                node = self.tree.root
        self.usertext.setPlainText(''.join(usertext))
        self.comtext.setPlainText("")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(758, 222)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Encode = QtWidgets.QPushButton(self.centralwidget)
        self.Encode.setGeometry(QtCore.QRect(310, 30, 151, 51))
        self.Encode.setStyleSheet("QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #6a11cb, stop:1 #2575fc); \n"
"    border: 2px solid #6a11cb;\n"
"    color: white;\n"
"    padding: 12px 24px; \n"
"    font-size: 14px; \n"
"    font-weight: bold; \n"
"    border-radius: 8px; \n"
"    text-transform: uppercase;\n"
"    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);\n"
"    transition: background-color 0.3s ease, transform 0.2s ease;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #2575fc, stop:1 #6a11cb);\n"
"    transform: translateY(-2px);\n"
"    box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.15); \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #2575fc, stop:1 #6a11cb);\n"
"    transform: translateY(0);\n"
"    box-shadow: 0px 3px 5px rgba(0, 0, 0, 0.2);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #cccccc;\n"
"    border: 2px solid #999999;\n"
"    color: #666666;\n"
"    box-shadow: none;\n"
"}")
        self.Encode.setObjectName("Encode")
        self.UserINP = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.UserINP.setGeometry(QtCore.QRect(20, 20, 281, 151))
        self.UserINP.setStyleSheet("QPlainTextEdit {\n"
"    background-color: #f9f9f9;\n"
"    border: 2px solid #cccccc;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"    selection-background-color: #6a11cb;\n"
"    selection-color: white;\n"
"    box-shadow: inset 0px 2px 4px rgba(0, 0, 0, 0.05);\n"
"}\n"
"\n"
"QPlainTextEdit:focus {\n"
"    border: 2px solid #6a11cb;\n"
"    background-color: #ffffff;\n"
"    box-shadow: inset 0px 2px 4px rgba(0, 0, 0, 0.1), 0px 0px 8px rgba(106, 17, 203, 0.2);\n"
"}\n"
"\n"
"QPlainTextEdit:disabled {\n"
"    background-color: #e0e0e0;\n"
"    border: 2px solid #999999;\n"
"    color: #666666;\n"
"}")
        self.UserINP.setReadOnly(False)
        self.UserINP.setPlainText("")
        self.UserINP.setObjectName("UserINP")
        self.Decode = QtWidgets.QPushButton(self.centralwidget)
        self.Decode.setGeometry(QtCore.QRect(310, 110, 151, 51))
        self.Decode.setStyleSheet("QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #6a11cb, stop:1 #2575fc);\n"
"    border: 2px solid #6a11cb;\n"
"    color: white;\n"
"    padding: 12px 24px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border-radius: 8px;\n"
"    text-transform: uppercase;\n"
"    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);\n"
"    transition: background-color 0.3s ease, transform 0.2s ease; \n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #2575fc, stop:1 #6a11cb);\n"
"    transform: translateY(-2px); /* Slight lift on hover */\n"
"    box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.15);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #2575fc, stop:1 #6a11cb);\n"
"    transform: translateY(0);\n"
"    box-shadow: 0px 3px 5px rgba(0, 0, 0, 0.2);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #cccccc;\n"
"    border: 2px solid #999999;\n"
"    color: #666666;\n"
"    box-shadow: none;\n"
"}")
        self.Decode.setObjectName("Decode")
        self.Compressed = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.Compressed.setGeometry(QtCore.QRect(470, 20, 281, 151))
        self.Compressed.setStyleSheet("QPlainTextEdit {\n"
"    background-color: #f9f9f9;\n"
"    border: 2px solid #cccccc;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"    selection-background-color: #6a11cb;\n"
"    selection-color: white;\n"
"    box-shadow: inset 0px 2px 4px rgba(0, 0, 0, 0.05);\n"
"}\n"
"\n"
"QPlainTextEdit:focus {\n"
"    border: 2px solid #6a11cb;\n"
"    background-color: #ffffff;\n"
"    box-shadow: inset 0px 2px 4px rgba(0, 0, 0, 0.1), 0px 0px 8px rgba(106, 17, 203, 0.2);\n"
"}\n"
"\n"
"QPlainTextEdit:disabled {\n"
"    background-color: #e0e0e0;\n"
"    border: 2px solid #999999;\n"
"    color: #666666;\n"
"}")
        self.Compressed.setReadOnly(True)
        self.Compressed.setObjectName("Compressed")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 758, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.huffman = huffmanalgo(self.UserINP,self.Compressed)
        self.Encode.clicked.connect(self.huffman.Encoder)
        self.Decode.clicked.connect(self.huffman.Decoder)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Encode.setText(_translate("MainWindow", "فشرده سازی ->"))
        self.Decode.setText(_translate("MainWindow", "<-رمز گشایی"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())