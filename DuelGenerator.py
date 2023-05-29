import sys
import os
import random
from Utils import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter, QPushButton, QDesktopWidget, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QColor, QPainter, QBrush


app = QApplication(sys.argv)

with open("output.txt", "r") as file:
    lines = file.readlines()

lines = [line.strip() for line in lines if line.strip()]
query1, query2 = random.sample(lines, k=2)

filter_list_path = os.path.join(os.getcwd(), "ublock_origin_filter_list.txt")

urls = ["https://www.youtube.com/results?search_query=" + query1, "https://www.youtube.com/results?search_query=" + query2]

os.environ["QWEBENGINEPROFILE_FILTERS_PATH"] = filter_list_path

browser = WebBrowser(urls)
browser.showMaximized()

sys.exit(app.exec_())
