import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt

class CustomButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)

        self.setFixedHeight(60)
        self.setFixedWidth(300)

        font = self.font()
        font.setPointSize(12)
        font.setBold(True)
        self.setFont(font)

        self.setStyleSheet("color: white; background-color: #4b3f7f; border-radius: 10px;")


class WebBrowser(QMainWindow):
    def __init__(self, games):
        super().__init__()

        self.setWindowTitle("Video Game Music Tournament")

        self.centralWidget = QWidget(self)  # Create a central widget to hold columns
        self.setCentralWidget(self.centralWidget)

        self.main_layout = QVBoxLayout(self.centralWidget)  # Main layout to hold rounds

        self.games = games  # Store the list of games
        self.current_game1 = 0  # Initialize the index for the first game
        self.current_game2 = 1  # Initialize the index for the second game

        # Open URLs for the first round
        self.load_round()

    def load_round(self):
        # Clear the current round layout
        while self.main_layout.count() > 0:
            item = self.main_layout.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.setParent(None)

        # Check if there are at least two games remaining
        if self.current_game2 < len(self.games):
            round_layout = QHBoxLayout()  # Create a layout for each round

            # Create a new round with the next pair of games
            # Create a new round with the next pair of games
            game1 = self.games[self.current_game1].strip()
            game2 = self.games[self.current_game2].strip()

            urls = [f"https://www.youtube.com/results?search_query={game1}", f"https://www.youtube.com/results?search_query={game2}"]

            for url, game in zip(urls, [game1, game2]):
                column_widget = QWidget()
                column_layout = QVBoxLayout(column_widget)
                column_widget.setStyleSheet("background-color: #ffffff;")

                web_view = QWebEngineView()
                web_view.load(QUrl(url))

                column_layout.addWidget(web_view)

                button = CustomButton(game)  # Set the game name as the button text
                button.clicked.connect(self.on_choose_button_clicked)  # Connect the button click event
                column_layout.addWidget(button, alignment=Qt.AlignHCenter)

                round_layout.addWidget(column_widget)

            self.main_layout.addLayout(round_layout)

    def on_choose_button_clicked(self):
        # Determine the winner based on which button was clicked
        if chosen_game == self.games[self.current_game1].strip():
            winner_index = self.current_game1
            loser_index = self.current_game2
        else:
            winner_index = self.current_game2
            loser_index = self.current_game1

        winner_game = self.games[winner_index].strip()

        # Display the chosen winner (for debugging purposes)
        print("Winner Game:", winner_game)

        # Write the winner to the "round_1.txt" file
        with open("../output/round_1.txt", "a") as file:
            file.write(winner_game + "\n")

        # Increment the game indices by 2 to load the next pair of games
        self.current_game1 += 2
        self.current_game2 += 2

        # Load the next round with the new pair of games
        self.load_round()
        
        
    def on_choose_button_clicked(self):
        # Determine the winner based on which button was clicked
        if self.sender().text() == "Choose":
            winner_index = self.current_game1
            loser_index = self.current_game2
        else:
            winner_index = self.current_game2
            loser_index = self.current_game1

        winner_game = self.games[winner_index].strip()

        # Write the winner to the "round_1.txt" file
        with open("../output/round_1.txt", "a") as file:
            file.write(winner_game + "\n")

        # Increment the game indices by 2 to load the next pair of games
        self.current_game1 += 2
        self.current_game2 += 2

        # Load the next round with the new pair of games
        self.load_round()
        
if __name__ == '__main__':
    # Read the game names from a file and shuffle them
    with open("../output/output.txt", "r") as file:
        games = file.readlines()
    random.shuffle(games)

    # Create a PyQt application
    app = QApplication(sys.argv)

    # Create an instance of the WebBrowser and show the window
    web_browser = WebBrowser(games)
    web_browser.showMaximized()

    # Start the application event loop
    sys.exit(app.exec_())