import sys
from PySide6.QtGui import * 
from PySide6.QtWidgets import * 
from PySide6.QtCore import * 

import keyboard

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
        self.result_display.setReadOnly(True) # Make read-only
        self.result_display.setAlignment(Qt.AlignRight) # Align text to right
        self.result_display.setFixedHeight(70) # Set fixed height
        self.result_display.setStyleSheet("font-size: 32px;")
        self.layout.addWidget(self.result_display)
        
        # Button layout
        self.buttons = [    
            ['+/-', 'C', '⌫'],
            ['x²', '√', '1/x', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['.', '0', '=']
        ]
        
        self.button_layout = QGridLayout()
        self.layout.addLayout(self.button_layout)
        
        self.button_map = {}
        
        for row, button_row in enumerate(self.buttons): # row index, button row
            for col, button_text in enumerate(button_row): # column index, button text
                button = QPushButton(button_text)
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # Set button size policy
                button.setStyleSheet("font-size: 24px;")
                if button_text == "⌫": # wide backspace block
                    self.button_layout.addWidget(button, row, col, 1, 2)
                elif button_text == "=": # wide "=" block
                    self.button_layout.addWidget(button, row, col, 1, 2)
                else:
                    col_offset = 1 if col > 0 and self.buttons[row][col - 1] == "⌫" else 0 # Shift columns if "⌫" button is found in the row
                    self.button_layout.addWidget(button, row, col + col_offset)
                
                button.clicked.connect(self.on_button_clicked) # Connect button click event to on_button_clicked method
                self.button_map[button_text] = button 
        
        self.current_expression = ""
        
        self.setup_key_bindings() # Set up key bindings
    
    # Set up key bindings
    def setup_key_bindings(self): 
        key_map = { # Key mapping
            '1': '1', '2': '2', '3': '3', 
            '4': '4', '5': '5', '6': '6', 
            '7': '7', '8': '8', '9': '9', 
            '0': '0',
            '+': '+', '-': '-', '*': '*', 
            '.': '.', '/': '/', 'enter': '=', 
            'backspace': '⌫'
        }
        
        # Bind key press event to button click event
        for key, button_text in key_map.items(): 
            keyboard.on_press_key(key, lambda e, bt = button_text: self.button_map[bt].click()) 
    
    # Button click event handler
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
        elif text == "x²": # squaring
            try:
                result = str(eval(f"{self.current_expression}**2"))
                self.result_display.setText(result)
                self.current_expression = result
            except Exception as e:
                self.result_display.setText("Error")
                self.current_expression = ""
        elif text == "√": # square root
            try:
                result = str(eval(f"{self.current_expression}**0.5"))
                self.result_display.setText(result)
                self.current_expression = result
            except Exception as e:
                self.result_display.setText("Error")
                self.current_expression = ""
        elif text == "1/x": # reciprocal
            try:
                result = str(eval(f"1/{self.current_expression}"))
                self.result_display.setText(result)
                self.current_expression = result
            except Exception as e:
                self.result_display.setText("Error")
                self.current_expression = ""
        else:
            self.current_expression += text
            self.result_display.setText(self.current_expression)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())
