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
    def __init__(self, urls, games):
        super().__init__()

        self.setWindowTitle("URL Columns")

        # Create a main widget and layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Set dark background color
        main_widget.setStyleSheet("background-color: #ffffff;")

        # Create a splitter to divide the window into columns
        splitter = QSplitter()
        layout.addWidget(splitter)

        self.columns = []  # Store the column widgets
        round = 2

        # Open URLs in columns
        for i, url in enumerate(urls):
            # Create a new column widget
            column_widget = QWidget()
            column_layout = QVBoxLayout(column_widget)

            # Set dark background color for column widget
            column_widget.setStyleSheet("background-color: #ffffff;")

            # Create a web view for the URL
            web_view = QWebEngineView()
            web_view.load(QUrl(url))

            # Inject CSS for dark mode
            self.dark_theme(web_view)

            column_layout.addWidget(web_view)

            # Create a button for the column
            button = CustomButton("Choose")
            column_layout.addWidget(button, alignment=Qt.AlignHCenter)

            # Connect button clicked signal to confirmation prompt
            button.clicked.connect(lambda checked, btn=button, game=games[i]: self.confirmation_prompt(btn, game, round))

            splitter.addWidget(column_widget)

            self.columns.append(column_widget)

    def reload_columns(self, games,round):
        for i, column_widget in enumerate(self.columns):
            column_layout = column_widget.layout()
            web_view = column_layout.itemAt(0).widget()
            button = column_layout.itemAt(1).widget()

            # Update the game for the button
            button.clicked.disconnect()  # Disconnect previous signal
            button.clicked.connect(lambda checked, btn=button, game=games[i]: self.confirmation_prompt(btn, game, 2))

            # Reload the web view with the updated URL
            url = "https://www.youtube.com/results?search_query=" + games[i * 2]
            web_view.load(QUrl(url))

    def dark_theme(self, web_view):
        script = """
            var css = 'body.ytd-app { background-color: #212121 !important; color: #212121 !important; }';
            var style = document.createElement('style');
            style.appendChild(document.createTextNode(css));
            document.head.appendChild(style);
            """
        web_view.page().runJavaScript(script)



    def confirmation_prompt(self, button, chosen_game, round):
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
            print("Option chosen:", chosen_game)

            with open(f"round_{round}.txt", "a") as file:
                file.write(chosen_game + "\n")
        else:
            print("Option not chosen")

        

