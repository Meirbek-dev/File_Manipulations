#!/usr/bin/env python3
# coding=utf-8

import re
import sys

import PyQt6.QtWidgets
from PyQt6.uic import loadUi

list_of_numbers = []


class Main(PyQt6.QtWidgets.QDialog):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('main.ui', self)

        # self.setWindowTitle('Работа с массивами и файлами PyQt6') Установка титула окна
        # self.setWindowIcon(QtGui.QIcon('logo.png')) Установка логотипа окна

        # Призывание кнопок к функциям при нажатии
        self.btn_upload_data.clicked.connect(self.upload_data_from_file)
        self.btn_process_data.clicked.connect(self.process_data)
        self.btn_save_data.clicked.connect(self.save_data)
        self.btn_clear.clicked.connect(self.clear)

    def upload_data_from_file(self):  # Метод загрузки данных из файла
        global path_to_file
        path_to_file = PyQt6.QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть файл', "", "Text Files (*.txt)")[0]
        if path_to_file:  # Нужно для того, чтобы программа не крашилась при отмене выбора файла
            file = open(path_to_file, 'r')  # Открытие файла в режиме чтения
            data = file.read()  # Чтение данных из файла
            self.plainTextEdit.appendPlainText("Полученные данные:\n" + data + "\n")
            global list_of_numbers
            list_of_numbers = []
            # \b -- ищет границы слов
            # [0-9] -- описывает что ищем
            # + -- говорит, что искать нужно минимум от 1 символа
            for num in re.findall(r'\b[0-9]+\b', data):
                list_of_numbers.append(int(num))

    def process_data(self):  # Метод обработки данных из файла
        if validation_of_data():  # Подтверждение того, что в файле действительно 30 числовых элементов
            last_row = list_of_numbers[-5:]
            max_num = find_max()
            if max_num in last_row:
                double_numbers()
                self.plainTextEdit.appendPlainText("Данные обработаны! " + '\n')
                # Вывод массива на экран
                for num in list_of_numbers:
                    self.plainTextEdit.insertPlainText(str(num) + " ")  # Добавление пробела после каждого числа
                    # Перенос на новую строко после каждого 5 элемента
                    if int(num) % 5 == 0:
                        self.plainTextEdit.appendPlainText("")
            else:
                self.plainTextEdit.appendPlainText(
                    "Максимальный элемент таблицы не в последней строке таблицы!\n")
        else:
            self.plainTextEdit.appendPlainText(
                "Неправильно введены данные!\nТаблица должна быть размером\n5х6 и состоять только из чисел!\n")

    def save_data(self):  # Метод сохранения данных в файл
        try:
            if path_to_file:
                file = open('output.txt', 'w')  # Открытие файла в режиме записи
                print(list_of_numbers)
                for n, num in enumerate(list_of_numbers):
                    file.write(str(num) + ' ')  # Запись каждого элемента массива через пробел
                    if (n + 1) % 5 == 0:  # Добавление переноса строки через каждые 5 элементов
                        file.write("\n")
                file.close()
                self.plainTextEdit.appendPlainText("Файл был успешно загружен!\n")
        except Exception:
            self.plainTextEdit.appendPlainText("Для начала загрузите файл!")

    def clear(self):
        self.plainTextEdit.clear()


def validation_of_data():  # Проверка, что в исходном файле ровно 30 чисел
    if len(list_of_numbers) == 30:
        for num in list_of_numbers:
            try:
                int(num)
            except Exception:
                return False
        return True
    else:
        return False


def find_max():  # Метод нахождения максимального элемента массива
    max_num = float('-inf')
    for num in list_of_numbers:
        if max_num < int(num):
            max_num = int(num)
    return max_num


def double_numbers():  # Удвоение всех элементов первого столбца в два раза
    for n, num in enumerate(list_of_numbers):
        first_col = (0, 5, 10, 15, 20, 25)
        if n in first_col:
            list_of_numbers[n] *= 2


if __name__ == '__main__':
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
