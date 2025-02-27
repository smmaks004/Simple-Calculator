import sys
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 400, 500)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setAlignment(Qt.AlignRight)
        self.result_display.setFixedHeight(70)
        self.result_display.setStyleSheet("font-size: 32px;")
        self.layout.addWidget(self.result_display)
        
        self.buttons = [
            ['C',  '⌫',' ', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['+/-', '0', '.', '=']
        ]
        
        self.button_layout = QGridLayout()
        self.layout.addLayout(self.button_layout)
        
        for row, button_row in enumerate(self.buttons):
            for col, button_text in enumerate(button_row):
                button = QPushButton(button_text)
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.setStyleSheet("font-size: 24px;")
                if button_text == "⌫":
                    self.button_layout.addWidget(button, row, col)
                    button.setStyleSheet("color:red;")
                else:
                    self.button_layout.addWidget(button, row, col)
                
                button.clicked.connect(self.on_button_clicked)
        
        self.current_expression = ""
    
    def on_button_clicked(self):
        button = self.sender()
        text = button.text()
        
        if text == "=":
            try:
                result = str(eval(self.current_expression))
                self.result_display.setText(result)
                self.current_expression = result
            except Exception as e:
                self.result_display.setText("Error")
                self.current_expression = ""
        elif text == "C":
            self.current_expression = ""
            self.result_display.setText(self.current_expression)
        # elif text == "CE":
        #     self.result_display.setText("") ###########
        elif text == "⌫":
            self.current_expression = self.current_expression[:-1]
            self.result_display.setText(self.current_expression)
        elif text == "+/-":
            if self.current_expression:
                if self.current_expression[0] == '-':
                    self.current_expression = self.current_expression[1:]
                else:
                    self.current_expression = '-' + self.current_expression
                self.result_display.setText(self.current_expression)
        else:
            self.current_expression += text
            self.result_display.setText(self.current_expression)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())