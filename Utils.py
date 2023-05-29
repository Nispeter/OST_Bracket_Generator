import sys
import os
import random
import Utils
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter, QPushButton, QDesktopWidget, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt, QPoint
from PyQt5.QtGui import QColor, QPainter, QBrush

class CustomButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)

        self.setFixedHeight(40)
        self.setFixedWidth(120)

        font = self.font()
        font.setPointSize(12)
        font.setBold(True)
        self.setFont(font)

        color = QColor(255, 255, 255)
        self.setStyleSheet("color: {}; background-color: {}; border-radius: 10px;".format(color.name(), QColor(75, 63, 127).name()))

class WebBrowser(QMainWindow):
    def __init__(self, urls):
        super().__init__()

        self.setWindowTitle("URL Columns")

        # Create a main widget and layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Set dark background color
        main_widget.setStyleSheet("background-color: #ffffff;")

        # Create a splitter to divide the window into two columns
        splitter = QSplitter()
        layout.addWidget(splitter)

        # Open URLs in columns
        for url in urls:
            # Create a new column widget
            column_widget = QWidget()
            column_layout = QVBoxLayout(column_widget)

            # Set dark background color for column widget
            column_widget.setStyleSheet("background-color: #ffffff;")

            # Create a web view for the URL
            web_view = QWebEngineView()
            web_view.load(QUrl(url))

            # Inject CSS for dark mode
            script = """
            var css = 'body.ytd-app { background-color: #212121 !important; color: #212121 !important; }';
            var style = document.createElement('style');
            style.appendChild(document.createTextNode(css));
            document.head.appendChild(style);
            """
            web_view.page().runJavaScript(script)

            column_layout.addWidget(web_view)

            # Create a button for the column
            button = CustomButton("Choose")
            column_layout.addWidget(button, alignment=Qt.AlignHCenter)

            # Connect button clicked signal to confirmation prompt
            button.clicked.connect(lambda checked, btn=button: self.confirmation_prompt(btn))

            splitter.addWidget(column_widget)

    def confirmation_prompt(self, button):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirmation")
        msg_box.setText("Are you sure you want to choose this option?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        # Calculate the position of the message box
        button_pos = button.mapToGlobal(button.rect().topLeft())
        msg_box_height = msg_box.sizeHint().height()
        msg_box_pos = button_pos - self.pos() - QPoint(0, msg_box_height)

        msg_box.move(msg_box_pos)

        if msg_box.exec_() == QMessageBox.Yes:
            print("Option chosen")
        else:
            print("Option not chosen")

