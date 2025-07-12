from PyQt6.QtWidgets import QWidget , QLabel , QLineEdit , QGridLayout ,QApplication , QPushButton,\
    QGridLayout
import sys

from datetime import datetime

class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()

        # Set the title
        self.setWindowTitle("Age Calculator")
        grid = QGridLayout()

        # Create widgets 
        name = QLabel("Name :")
        self.name_line = QLineEdit()
        birth = QLabel("Your birth DD-MM-YYYY:")
        self.birth_line = QLineEdit()
        age_button = QPushButton("age calculate")
        age_button.clicked.connect(self.calculate_age)
        self.output  = QLabel("")
        self.error = QLabel("")

        # Add the widgets in application
        grid.addWidget(name , 0 , 0 )
        grid.addWidget(self.name_line , 0 , 1)
        grid.addWidget(birth , 1 , 0)
        grid.addWidget(self.birth_line , 1 , 1)
        grid.addWidget(age_button , 2 , 0 , 1 , 2)
        grid.addWidget(self.output , 3 , 0 , 1 , 2)
        grid.addWidget(self.error , 3 , 0 , 1 , 2)

        self.setLayout(grid)

    def calculate_age(self):
        try:
            current_age = datetime.now().year
            user_birth = self.birth_line.text()
            year_birth = datetime.strptime(user_birth , "%d-%m-%Y").date().year
            birth_date = current_age - year_birth
            self.output.setText(f"{self.name_line.text().title()} age is {birth_date}")
            self.error.setText("")
        except(ValueError):
            self.output.setText("")
            self.error.setText("Please Enter properly")


app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
sys.exit(app.exec())


