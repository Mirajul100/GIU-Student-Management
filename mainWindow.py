from PyQt6.QtWidgets import QApplication , QLabel , QLineEdit , QPushButton , QGridLayout , QWidget,\
    QMainWindow , QTableWidget , QTableWidgetItem , QDialog , QVBoxLayout , QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setFixedHeight(300)
        self.setFixedWidth(414)

        file = self.menuBar().addMenu("&File")
        help = self.menuBar().addMenu("&Help")
        edit = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Add student" , self)
        add_student_action.triggered.connect(self.insert)
        file.addAction(add_student_action)

        add_about_action = QAction("About" , self)
        help.addAction(add_about_action)

        add_edit_action = QAction("Search" , self)
        add_edit_action.triggered.connect(self.search)
        edit.addAction(add_edit_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id" , "Name" , "Course" , "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def loadData(self):
        connection = sqlite3.connect("004 database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)

        for row_number , row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number , data in enumerate(row_data):
                self.table.setItem(row_number , column_number , QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog() 
        dialog.exec()
    
    def search(self):
        sd = SearchDialog()
        sd.exec()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Student Data")
        self.setFixedHeight(250)
        self.setFixedWidth(250)

        vlayout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")

        self.student_combo = QComboBox()
        item = ["Biology" , "Math" , "Physics" , "Chemistry"]
        self.student_combo.addItems(item)

        self.student_mobile = QLineEdit()
        self.student_mobile.setPlaceholderText("Mobile Number")

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.add_student)

        self.error = QLabel("")
        self.success = QLabel("")

        vlayout.addWidget(self.student_name)
        vlayout.addWidget(self.student_combo)
        vlayout.addWidget(self.student_mobile)
        vlayout.addWidget(submit_button)
        vlayout.addWidget(self.error)
        vlayout.addWidget(self.success)
        
        self.setLayout(vlayout)

    def add_student(self):
        name = self.student_name.text().title()
        course = self.student_combo.itemText(self.student_combo.currentIndex())
        mobile = self.student_mobile.text()

        if (name != "" and course != "" and mobile != ""):
                
            connection = sqlite3.connect("004 database.db")
            cursor = connection.cursor()
            cursor = cursor.execute("INSERT INTO students (name , course , mobile) VALUES (?, ?, ?)",
                                    (name , course , mobile))
            connection.commit()
            cursor.close()
            connection.close()
            main_window.loadData()
            self.error.setText("")
            self.success.setText("Successfully Enter The Student Information")

        else :
            self.success.setText("")
            self.error.setText("please fill properly") 

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student info")
        self.setFixedHeight(250)
        self.setFixedWidth(250)

        vlayout = QVBoxLayout()

        self.name_search = QLineEdit()
        self.name_search.setPlaceholderText("Name")
        vlayout.addWidget(self.name_search)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.info_search)
        vlayout.addWidget(search_button)

        self.setLayout(vlayout)

    def info_search(self):
        pass
        

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.loadData()
sys.exit(app.exec())