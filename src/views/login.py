import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLineEdit, QLabel, QPushButton
from PyQt6.QtCore import QRect

class LoginWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
    
    def __init_fonts(self) -> None:
        self.text_font = QtGui.QFont()
        self.title1_font = QtGui.QFont()
        self.title2_font = QtGui.QFont()
        
        self.text_font.setFamily("Poppins")
        
        self.title1_font.setFamily("Raleway SemiBold")
        self.title1_font.setPointSize(14)
        self.title1_font.setBold(True)
        
        self.title2_font.setFamily("Raleway Semibold")
        self.title2_font.setPointSize(24)
        self.title2_font.setBold(True)
    
    def __init_labels(self) -> None:
        self.username_label = QLabel(parent=self)
        self.password_label = QLabel(parent=self)
    
    def __init_fields(self) -> None:
        self.username_field = QLineEdit(parent=self)
        self.password_field = QLineEdit(parent=self)
        
        self.username_field.setText("")
        self.username_field.setEchoMode(QLineEdit.EchoMode.Normal)
        self.username_field.setObjectName("input_field")
        self.username_field.setGeometry(QRect(20, 230, 161, 22))
        
        self.password_field.setText("")
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_field.setObjectName("input_field")
        self.username_field.setGeometry(QRect(20, 230, 161, 22))
    
    def __init_buttons(self) -> None:
        self.login_button = QPushButton(parent=self)


class Ui_MainWindow(object):
    def __init__(self) -> None:
        pass
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(240, 438)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.login_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.login_frame.setGeometry(QtCore.QRect(0, 0, 241, 441))
        self.login_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.login_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.login_frame.setObjectName("login_frame")
        self.password_field = QtWidgets.QLineEdit(parent=self.login_frame)
        self.password_field.setGeometry(QtCore.QRect(20, 290, 161, 22))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        self.password_field.setFont(font)
        self.password_field.setText("")
        self.password_field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_field.setObjectName("password_field")
        self.username_field = QtWidgets.QLineEdit(parent=self.login_frame)
        self.username_field.setGeometry(QtCore.QRect(20, 230, 161, 22))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        self.username_field.setFont(font)
        self.username_field.setText("")
        self.username_field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.username_field.setObjectName("username_field")
        self.username_label = QtWidgets.QLabel(parent=self.login_frame)
        self.username_label.setGeometry(QtCore.QRect(20, 210, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        self.username_label.setFont(font)
        self.username_label.setObjectName("username_label")
        self.password_label = QtWidgets.QLabel(parent=self.login_frame)
        self.password_label.setGeometry(QtCore.QRect(20, 270, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")
        self.push_button = QtWidgets.QPushButton(parent=self.login_frame)
        self.push_button.setGeometry(QtCore.QRect(20, 350, 75, 24))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        self.push_button.setFont(font)
        self.push_button.setAcceptDrops(False)
        self.push_button.setAutoFillBackground(False)
        self.push_button.setAutoDefault(False)
        self.push_button.setDefault(False)
        self.push_button.setFlat(False)
        self.push_button.setObjectName("push_button")
        self.username_label_2 = QtWidgets.QLabel(parent=self.login_frame)
        self.username_label_2.setGeometry(QtCore.QRect(20, 100, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Raleway SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        self.username_label_2.setFont(font)
        self.username_label_2.setObjectName("username_label_2")
        self.username_label_3 = QtWidgets.QLabel(parent=self.login_frame)
        self.username_label_3.setGeometry(QtCore.QRect(20, 130, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Raleway SemiBold")
        font.setPointSize(24)
        font.setBold(True)
        self.username_label_3.setFont(font)
        self.username_label_3.setObjectName("username_label_3")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.username_label.setText(_translate("MainWindow", "Username"))
        self.password_label.setText(_translate("MainWindow", "Password"))
        self.push_button.setText(_translate("MainWindow", "Log In"))
        self.username_label_2.setText(_translate("MainWindow", "Welcome to"))
        self.username_label_3.setText(_translate("MainWindow", "MARITES"))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())