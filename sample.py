from PyQt6.QtWidgets import QWidget , QLabel , QLineEdit , QPushButton , QApplication , QComboBox ,\
    QGridLayout
import sys

class SpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Speed calculator")
        grid = QGridLayout()

        dis = QLabel("Distance : ")
        self.dis_line = QLineEdit()

        time = QLabel("Time : ")
        self.time_line = QLineEdit()

        self.combo = QComboBox()
        self.combo.addItems(['matrix (km)','imperial (miles)'])

        button = QPushButton("Calculate")
        button.clicked.connect(self.calculate)

        self.result = QLabel("")
        self.error = QLabel("")

        grid.addWidget(dis , 0 , 0)
        grid.addWidget(self.dis_line , 0 , 1)
        grid.addWidget(self.combo , 0 , 2)
        grid.addWidget(time , 1 , 0)
        grid.addWidget(self.time_line , 1 , 1)
        grid.addWidget(button , 2 , 1)
        grid.addWidget(self.result , 3 , 0 , 1 , 2)
        grid.addWidget(self.error , 3 , 0 , 1 , 2)

        self.setLayout(grid)

    def calculate(self):
        try:
            distance = float(self.dis_line.text())
            time = float(self.time_line.text())

            speed = distance / time

            if self.combo.currentText() == 'matrix (km)':
                speed = round(speed , 2)
                unit = "km/h"
            if self.combo.currentText() == 'imperial (miles)':
                speed = round(speed * 0.621371 , 2)
                unit = "mile"

            self.result.setText(f"Average speed : {speed} {unit}")
            self.error.setText("")
        except(ValueError):
            self.result.setText("")
            self.error.setText("Please enter properly")

app =  QApplication(sys.argv)
speed = SpeedCalculator()
speed.show()
sys.exit(app.exec())
