import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QComboBox, QCheckBox, QFileDialog, QProgressBar, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QMenu, QAction, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QCoreApplication
from PyQt5.QtGui import QCursor
from typing import Union, Optional
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFontDatabase
from Newdesign import Ui_MainWindow
from operator import add, sub, mul, truediv
import keyboard
import Calc_Library as cl
import time

operations = {
    "+": cl.Plus,
    "-": cl.Minus,
    # "*": cl.Multiply,
    # "/": cl.Divide,
    "×": cl.Multiply,
    "÷": cl.Divide,
}






error_zero_division = "You can't divide by zero!"
error_undifined = "Undefined!"
default_font_size = 16
default_entry_font_size = 40

class Calculator(QMainWindow):



    def __init__(self):
        self.keyboard_hook = None
        super(Calculator,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.entry_max_length = self.ui.entry.maxLength()

        self.unpressed = self.ui.Button_1.styleSheet()

        self.style_sheet_for_enable = self.ui.Button_Divide.styleSheet()
        QFontDatabase.addApplicationFont("Rubik\static\Rubik-Bold.ttf")

        self.ui.Button_0.clicked.connect(lambda: self.add_number("0"))
        self.ui.Button_1.clicked.connect(lambda: self.add_number("1"))
        self.ui.Button_2.clicked.connect(lambda: self.add_number("2"))
        self.ui.Button_3.clicked.connect(lambda: self.add_number("3"))
        self.ui.Button_4.clicked.connect(lambda: self.add_number("4"))
        self.ui.Button_5.clicked.connect(lambda: self.add_number("5"))
        self.ui.Button_6.clicked.connect(lambda: self.add_number("6"))
        self.ui.Button_7.clicked.connect(lambda: self.add_number("7"))
        self.ui.Button_8.clicked.connect(lambda: self.add_number("8"))
        self.ui.Button_9.clicked.connect(lambda: self.add_number("9"))

        #clears
        self.ui.Button_c.clicked.connect(self.clear_all)
        self.ui.Button_ce.clicked.connect(self.clear_entry)
        self.ui.Button_backspace.clicked.connect(self.backspace)
        #actions
        self.ui.Button_Comma.clicked.connect(self.add_point)
        self.ui.Button_Sign.clicked.connect(self.change_sign)

        #math
        self.ui.Button_Equal.clicked.connect(self.binary_calculate)
        self.ui.Button_Plus.clicked.connect(lambda: self.math_operation(' +'))
        self.ui.Button_Minus.clicked.connect(lambda: self.math_operation(' -'))
        self.ui.Button_Multiply.clicked.connect(lambda: self.math_operation(' ×'))
        self.ui.Button_Divide.clicked.connect(lambda: self.math_operation(' ÷'))
        self.ui.Button_Root.clicked.connect(lambda: self.math_operation(' √'))
        self.ui.Button_Power.clicked.connect(lambda: self.math_operation(' ^'))
        self.ui.Button_Factorial.clicked.connect(lambda: self.math_operation(' !'))

    def print_key_event(self, event) -> None:
        # print(event.name)
        pressed = ( "QPushButton {\n"
                    "border-bottom: 2px solid rgb(0, 148, 198);\n"
                    "border-left: 1rem solid rgb(0, 0, 0);\n"
                    "border-top: none;\n"
                    "border-right: none;\n"
                    "width: 5px;\n"
                    "color: #FFF;\n"
                    "background-color: #222;\n"
                    "border-radius: 10px;\n"
                    "background-color: #666;\n"
                    "border-bottom: 2px solid rgb(255, 255, 255);\n"
                    "color: #Dff;\n}")

        if event.name == '0':
            self.ui.Button_0.click()
        elif event.name == '1':
            self.ui.Button_1.click()
        elif event.name == '2':
            self.ui.Button_2.click()
        elif event.name == '3':
            self.ui.Button_3.click()
            # self.ui.Button_3.setStyleSheet(pressed)
            # time.sleep(0.5)
            # self.ui.Button_3.setStyleSheet(self.unpressed)
            # self.ui.Button_3.setShortcut('3')
        elif event.name == '4':
            self.ui.Button_4.click()
        elif event.name == '5':
            self.ui.Button_5.click()
        elif event.name == '6':
            self.ui.Button_6.click()
        elif event.name == '7':
            # self.ui.Button_7.clicked.connect(self.add_number("7"))
            self.ui.Button_7.click()
        elif event.name == '8':
            self.ui.Button_8.click()
        elif event.name == '9':
            self.ui.Button_9.click()
        elif event.name == 'enter':
            self.ui.Button_Equal.click()
        elif event.name == 'backspace':
            self.ui.Button_backspace.click()
        elif event.name == 'delete':
            self.ui.Button_c.click()
        elif event.name == '.':
            self.ui.Button_Comma.click()
        elif event.name == '+':
            print('plus pressed')
            self.ui.Button_Plus.click()
        elif event.name == '-':
            self.ui.Button_Minus.click()
        elif event.name == '*':
            self.ui.Button_Multiply.click()
        elif event.name == '/':
            self.ui.Button_Divide.click()


    # keyboard.on_press(lambda event: self.print_key_event(event))

    # def register_keyboard_event(self):
    #     self.keyboard_hook = keyboard.hook(self.print_key_event)
    #
    # def unregister_keyboard_event(self):
    #     keyboard.unhook(self.keyboard_hook)
    def register_keyboard_event(self):
        keyboard.on_press(lambda event: self.print_key_event(event))

    def add_number(self, Button_text: str) -> None:
        # self.remove_error()
        # self.clear_history_if_equality()
        if self.ui.entry.text() == "0":
            self.ui.entry.setText(Button_text)
        else:
            self.ui.entry.setText(self.ui.entry.text() + Button_text)

        self.adjust_entry_font_size()

    def add_point(self) -> None:
        self.clear_history_if_equality()
        if ',' not in self.ui.entry.text():
            self.ui.entry.setText(self.ui.entry.text() + ',')
            self.adjust_entry_font_size()

    def change_sign(self):
        entry = self.ui.entry.text()

        if '-' not in self.ui.entry.text():
            if entry != "0":
                entry = '-' + entry
        else:
            entry = entry[1:]

        if len(entry) == self.entry_max_length+1 and '-' in entry:
            self.ui.entry.setMaxLength(self.entry_max_length + 1)
        else:
            self.ui.entry.setMaxLength(self.entry_max_length)
        self.ui.entry.setText(entry)
        self.adjust_entry_font_size()

    def clear_all(self) -> None:
        self.remove_error()
        self.ui.entry.setText("0")
        self.ui.history.clear()

    def clear_entry(self) -> None:
        self.remove_error()
        self.clear_history_if_equality()
        self.ui.entry.setText("0")
        self.adjust_entry_font_size()

    def backspace(self) -> None:
        self.remove_error()
        self.clear_history_if_equality()
        entry = self.ui.entry.text()

        if len(entry) != 1:
            if len(entry) == 2 and '-' in entry:
                self.ui.entry.setText("0")
                self.adjust_entry_font_size()
            else:
                self.ui.entry.setText(entry[:-1])
                self.adjust_entry_font_size()
        else:
            self.ui.entry.setText("0")
            self.adjust_entry_font_size()

    def clear_history_if_equality(self) -> None:
        if self.get_history_sign() == '=':
            self.ui.history.clear()

    def add_history(self, math_sign: str):
       if not self.ui.history.text() or self.get_history_sign() == '=':
           history = self.remove_trailing_zeroes(self.ui.entry.text()) + f'{math_sign}'
           history = history.replace(".", ",")
           self.ui.history.setText(history)
           self.ui.entry.setText("0")
           self.adjust_entry_font_size()

    @staticmethod
    def remove_trailing_zeroes(number: str) -> str:
        n = str(number)
        n = n.replace(",", ".")
        n = str(float(n))
        return n[:-2] if n.endswith('.0') else n

    def get_entry_number(self) -> Union[int, float]:
        entry = self.ui.entry.text().strip(',')
        entry = entry.replace(",", ".")
        print(entry)
        return float(entry) if '.' in entry else int(entry)

    def get_history_number(self) -> Union[int, float, None]:
        history = self.ui.history.text().strip(',').split()[0]
        history = history.replace(",", ".")
        print(history)
        return float(history) if '.' in history else int(history)

    def get_history_sign(self) -> Optional[str]:
        if self.ui.history.text():
            return self.ui.history.text().strip(',').split()[-1]

    def get_entry_text_width(self) -> int:
        return self.ui.entry.fontMetrics().boundingRect(self.ui.entry.text()).width()

    def get_history_text_width(self) -> int:
        return self.ui.history.fontMetrics().boundingRect(self.ui.history.text()).width()

    def binary_calculate(self) -> Optional[str]:
        entry = self.ui.entry.text()
        temp = self.ui.history.text()
        if temp:
            try:
                result = self.remove_trailing_zeroes(
                    str(operations[self.get_history_sign()](self.get_history_number(), self.get_entry_number()))
                )
                result = result.replace(".", ",")
                history = temp + " " + self.remove_trailing_zeroes(entry) + " ="
                history = history.replace(".", ",")
                self.ui.history.setText(history)
                self.ui.entry.setText(result)
                self.adjust_entry_font_size()
                return result

            except KeyError:
                pass

            except ZeroDivisionError:
                if self.get_history_number() == 0:
                    self.show_error(error_undifined)
                else:
                    self.show_error(error_zero_division)

    def unary_calculate(self) -> Optional[str]:
        entry = self.ui.entry.text()
        temp = self.ui.history.text()
        if temp:
            try:
                result = self.remove_trailing_zeroes(
                    str(operations[self.get_history_sign()](self.get_history_number(), self.get_entry_number()))
                )
                result = result.replace(".", ",")
                history = temp + " " + self.remove_trailing_zeroes(entry) + " ="
                history = history.replace(".", ",")
                self.ui.history.setText(history)
                self.ui.entry.setText(result)
                self.adjust_entry_font_size()
                return result

            except KeyError:
                pass

            except ZeroDivisionError:
                if self.get_history_number() == 0:
                    self.show_error(error_undifined)
                else:
                    self.show_error(error_zero_division)

    def math_operation(self, math_sign: str):
        temp = self.ui.history.text()

        if not temp:
            self.add_history(math_sign)
        else:
            if self.get_history_sign() != math_sign:
                if self.get_history_sign() == '=':
                    self.add_history(math_sign)
                else:
                    self.ui.history.setText(temp[:-2] + f'{math_sign}')
            elif math_sign == 'fact' or math_sign == 'sqrt' or math_sign == 'sqr':
                self.ui.history.setText(self.unary_calculate() + f'{math_sign}')
            else:
                self.ui.history.setText(self.binary_calculate() + f'{math_sign}')

    def add_factorial(self):
        temp = self.ui.history.text()

        if not temp:
            self.add_history("!")
        else:
            if self.get_history_sign() != "!":
                if self.get_history_sign() == '=':
                    self.add_history("!")
                else:
                    self.ui.history.setText(temp[:-2] + f'{"!"}')
            else:
                self.ui.history.setText(self.binary_calculate() + f'{"!"}')


    def show_error(self, text: str) -> None:
        self.ui.entry.setMaxLength(len(text))
        self.ui.entry.setText(text)
        self.adjust_entry_font_size()
        self.disable_buttons(True)

    def remove_error(self) -> None:
        if self.ui.entry.text() in (error_undifined, error_zero_division):
            self.ui.entry.setMaxLength(self.entry_max_length)
            self.ui.entry.setText("0")
            self.adjust_entry_font_size()
            self.disable_buttons(False)

    def disable_buttons(self, disable: bool) -> None:
        self.ui.Button_Equal.setDisabled(disable)
        self.ui.Button_Plus.setDisabled(disable)
        self.ui.Button_Minus.setDisabled(disable)
        self.ui.Button_Multiply.setDisabled(disable)
        self.ui.Button_Divide.setDisabled(disable)
        self.ui.Button_Comma.setDisabled(disable)
        if disable:
            color =("border-bottom: 2px solid rgb(0, 148, 198);"
                    " border-left: 1rem solid rgb(0, 0, 0);"
                    "  border-top: none;"
                    "  border-right: none;"
                    "width: 5px;"
                    "color: #FFF;"
                    "background-color: #222;"
                    "border-radius: 10px;"
                    "color: #777;")
            self.change_buttons_color(color)
        else:
            self.return_buttons_color()

    def change_buttons_color(self, css_color: str) -> None:
        self.ui.Button_Equal.setStyleSheet(css_color)
        self.ui.Button_Plus.setStyleSheet(css_color)
        self.ui.Button_Minus.setStyleSheet(css_color)
        self.ui.Button_Multiply.setStyleSheet(css_color)
        self.ui.Button_Divide.setStyleSheet(css_color)
        self.ui.Button_Comma.setStyleSheet(css_color)

    def return_buttons_color(self) -> None:
        self.ui.Button_Equal.setStyleSheet(self.style_sheet_for_enable)
        self.ui.Button_Plus.setStyleSheet(self.style_sheet_for_enable)
        self.ui.Button_Minus.setStyleSheet(self.style_sheet_for_enable)
        self.ui.Button_Multiply.setStyleSheet(self.style_sheet_for_enable)
        self.ui.Button_Divide.setStyleSheet(self.style_sheet_for_enable)
        self.ui.Button_Comma.setStyleSheet(self.style_sheet_for_enable)

    def adjust_entry_font_size(self) -> None:
        font_size = default_entry_font_size
        while self.get_entry_text_width() > self.ui.entry.width() - 20:
            font_size -= 1
            self.ui.entry.setStyleSheet('font-size: ' + str(font_size) + 'pt; '
                                                                         'background-color: rgb(30, 30, 30); '
                                                                         'border: none; '
                                                                         'border-radius: 10px;')

        font_size = 1
        while self.get_entry_text_width() < self.ui.entry.width() - 20:
            font_size += 1

            if font_size > default_entry_font_size:
                break

            self.ui.entry.setStyleSheet('font-size: ' + str(font_size) + 'pt; '
                                                                         'background-color: rgb(30, 30, 30); '
                                                                         'border: none; '
                                                                         'border-radius: 10px;')

    def resizeEvent(self, event) -> None:
        self.adjust_entry_font_size()

# calc = Calculator()
# calc.register_keyboard_event()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    window.register_keyboard_event()
    sys.exit(app.exec())

