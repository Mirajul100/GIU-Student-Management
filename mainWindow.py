from PyQt6.QtWidgets import QApplication , QLabel , QLineEdit , QPushButton , QGridLayout , QWidget,\
    QMainWindow , QTableWidget , QTableWidgetItem , QDialog , QVBoxLayout , QComboBox , QToolBar , QStatusBar
from PyQt6.QtGui import QAction , QIcon
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Student Management System")
        self.setWindowIcon(QIcon("image/home.png"))
        self.resize(414 , 400)
        self.move(100 , 200)

        file = self.menuBar().addMenu("&File")
        help = self.menuBar().addMenu("&Help")
        edit = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("image/add.png"),"Add student" , self)
        add_student_action.triggered.connect(self.insert)
        file.addAction(add_student_action)

        add_about_action = QAction("About" , self)
        help.addAction(add_about_action)

        add_edit_action = QAction(QIcon("image/search.png"),"Id Search" , self)
        add_edit_action.triggered.connect(self.search)
        edit.addAction(add_edit_action)

        add_name_action = QAction("Name Search" , self)
        add_name_action.triggered.connect(self.name_search)
        edit.addAction(add_name_action)

        add_course_action = QAction("Course Search" , self)
        add_course_action.triggered.connect(self.course_data_search)
        edit.addAction(add_course_action)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        toolbar.addAction(add_student_action)
        toolbar.addAction(add_edit_action)
        self.addToolBar(toolbar)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

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

        value = QLabel(f"Total student number is : {row_number + 1}")
        self.statusbar.addWidget(value)

    def insert(self):
        dialog = InsertDialog() 
        dialog.exec()
    
    def search(self):
        sd = SearchDialog()
        sd.exec()
    
    def name_search(self):
        ns = NameSearchDialog()
        ns.exec()

    def course_data_search(self):
        cs = CourseDialog()
        cs.exec()

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
        if (student_info == ""):
            self.error = ErrorDialog()
            self.error.exec()

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
        if (student_name != ""):
            self.name_info_table = InfoTable()
            self.name_info_table.name_info(student_name)
            self.name_info_table.show()
        if (student_name == ""):
            self.error = ErrorDialog()
            self.error.exec()

class CourseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Course Search")
        self.resize(250 , 250)
        self.move(1030 , 200)

        vlayout = QVBoxLayout()

        self.course_search = QLineEdit()
        self.course_search.setPlaceholderText("Enter the course")
        vlayout.addWidget(self.course_search)

        course_search_button = QPushButton("Search")
        course_search_button.clicked.connect(self.course)
        vlayout.addWidget(course_search_button)

        self.setLayout(vlayout)

    def course(self):
        course_name = self.course_search.text().title()
        if (course_name != ""):
            self.course_info = InfoTable()
            self.course_info.course_data(course_name)
            self.course_info.show()
        if (course_name == ""):
            self.error = ErrorDialog()
            self.error.exec()

class ErrorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERROR!")
        self.resize(150 , 40)
        self.move(1030 , 500)

        vlayout = QVBoxLayout()

        self.error = QLabel("PLEASE ENTER PROPERLY")
        vlayout.addWidget(self.error)
        self.setLayout(vlayout)

class SuccessfulDialog(QDialog):
     def __init__(self):
        super().__init__()
        self.setWindowTitle("SUCCESSFUL")
        self.resize(150 , 40)
        self.move(1030 , 500)

        vlayout = QVBoxLayout()

        self.successful = QLabel("ENTER SUCCESSFULLY")
        vlayout.addWidget(self.successful)
        self.setLayout(vlayout)

class InfoTable(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Selected student info")
        self.setWindowIcon(QIcon("image/icon.png"))
        self.resize(414 , 400)
        self.move(562 , 200)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id" , "Name" , "Course" , "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

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
        try:
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
            
            value = QLabel(f"Total student of same name : {row_num + 1}")
            self.status.addWidget(value)
        except(UnboundLocalError):
            value = QLabel(f"There are no student in name of {self.name}")
            self.status.addWidget(value)

    def course_data(self , course_name):
        try:
            self.c_name = course_name
            connection = sqlite3.connect("004 database.db")
            cursor = connection.cursor()
            result = cursor.execute("SELECT * FROM students WHERE course = ?" , (self.c_name,))
            self.table.setRowCount(0)

            for row_num , row_data in enumerate(result):
                self.table.insertRow(row_num)
                for col_num , data in enumerate(row_data):
                    self.table.setItem(row_num , col_num , QTableWidgetItem(str(data)))
            cursor.close()
            connection.close()

            value = QLabel(f"Total number of student enroll in {self.c_name} is : {row_num + 1}")
            self.status.addWidget(value)
        except(UnboundLocalError): 
            value = QLabel(f"{self.c_name} course if not available")
            self.status.addWidget(value)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.loadData()
sys.exit(app.exec())