from PyQt6.QtWidgets import QApplication , QLabel , QLineEdit , QPushButton , QGridLayout , QWidget,\
    QMainWindow , QTableWidget , QTableWidgetItem , QDialog , QVBoxLayout , QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.resize(414 , 300)
        self.move(100 , 200)

        file = self.menuBar().addMenu("&File")
        help = self.menuBar().addMenu("&Help")
        edit = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Add student" , self)
        add_student_action.triggered.connect(self.insert)
        file.addAction(add_student_action)

        add_about_action = QAction("About" , self)
        help.addAction(add_about_action)

        add_edit_action = QAction("Id Search" , self)
        add_edit_action.triggered.connect(self.search)
        edit.addAction(add_edit_action)

        add_name_action = QAction("Name Search" , self)
        add_name_action.triggered.connect(self.name_search)
        edit.addAction(add_name_action)

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
    
    def name_search(self):
        ns = NameSearchDialog()
        ns.exec()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Student Data")
        self.resize(250 , 250)
        self.move(1000 , 200)

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

        vlayout.addWidget(self.student_name)
        vlayout.addWidget(self.student_combo)
        vlayout.addWidget(self.student_mobile)
        vlayout.addWidget(submit_button)
        
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
            str_success = SuccessfulDialog()
            str_success.exec()

        else :
            str_error = ErrorDialog()
            str_error.exec()

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student info")
        self.resize(250 , 250)
        self.move(1030 , 200)

        vlayout = QVBoxLayout()

        self.id_search = QLineEdit()
        self.id_search.setPlaceholderText("Enter ID")
        vlayout.addWidget(self.id_search)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.info_search)
        vlayout.addWidget(search_button)

        self.setLayout(vlayout)

    def info_search(self):
        student_info = self.id_search.text()
        if student_info.strip():
            self.info_table = InfoTable()
            self.info_table.info_data(student_info)
            self.info_table.show()

class NameSearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student info")
        self.resize(250 , 250)
        self.move(1030 , 200)

        vlayout = QVBoxLayout()

        self.st_name = QLineEdit()
        self.st_name.setPlaceholderText("Enter the name")
        vlayout.addWidget(self.st_name)

        st_button = QPushButton("Search")
        st_button.clicked.connect(self.name_info_search)
        vlayout.addWidget(st_button)

        self.setLayout(vlayout)

    def name_info_search(self):
        student_name = self.st_name.text().title()
        if (student_name != None):
            self.name_info_table = InfoTable()
            self.name_info_table.name_info(student_name)
            self.name_info_table.show()

class ErrorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERROR!")
        self.resize(150 , 40)
        self.move(1000 , 500)

        vlayout = QVBoxLayout()

        error = QLabel("PLEASE ENTER PROPERLY")
        vlayout.addWidget(error)

class SuccessfulDialog(QDialog):
     def __init__(self):
        super().__init__()
        self.setWindowTitle("SUCCESSFUL")
        self.resize(150 , 40)
        self.move(1000 , 500)

        vlayout = QVBoxLayout()

        successful = QLabel("ENTER SUCCESSFULLY")
        vlayout.addWidget(successful)

class InfoTable(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Selected student info")
        self.setFixedHeight(200)
        self.setFixedWidth(412)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id" , "Name" , "Course" , "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def info_data(self , student_id):
        self.id = student_id
        connection = sqlite3.connect("004 database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE id = ?" , (self.id,))
        self.table.setRowCount(0)

        for row_num , row_data in enumerate(result):
            self.table.insertRow(row_num)
            for col_num , data in enumerate(row_data):
                self.table.setItem(row_num , col_num , QTableWidgetItem(str(data)))
        cursor.close()
        connection.close()
    
    def name_info(self , student_name):
        self.name = student_name
        connection = sqlite3.connect("004 database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?" , (self.name,))
        self.table.setRowCount(0)

        for row_num , row_data in enumerate(result):
            self.table.insertRow(row_num)
            for col_num , col_data in enumerate(row_data):
                self.table.setItem(row_num , col_num , QTableWidgetItem(str(col_data)))
        cursor.close()
        connection.close()
        

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.loadData()
sys.exit(app.exec())