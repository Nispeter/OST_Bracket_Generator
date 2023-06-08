import sys
import os
import random
from Utils import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter, QPushButton, QDesktopWidget, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QColor, QPainter, QBrush


# get lines on game file and shuffle 
with open("output.txt", "r") as file:
    lines = file.readlines()

random.shuffle(lines)

# Overwrite output.txt with shuffled lines
with open("round_1.txt", "w") as file:
    file.writelines(lines)

app = QApplication(sys.argv)

# Read the shuffled lines from output.txt, and stip them of lines list
lines = [line.strip() for line in lines if line.strip()]

# Extract the first two lines as query1 and query2
query1, query2 = lines[:2]

filter_list_path = os.path.join(os.getcwd(), "ublock_origin_filter_list.txt")

# Queries made of read lines 
urls = ["https://www.youtube.com/results?search_query=" + query1, "https://www.youtube.com/results?search_query=" + query2]

os.environ["QWEBENGINEPROFILE_FILTERS_PATH"] = filter_list_path

# UI
browser = WebBrowser(urls,lines)
# Screen config
browser.showMaximized()

sys.exit(app.exec_())