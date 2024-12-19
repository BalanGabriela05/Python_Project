import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QSpacerItem, QSizePolicy, QHBoxLayout, QInputDialog
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from database.Connection import get_db
from SeriesService import add_series
from Validation import is_valid_link_imdb, is_valid_episode_format, is_valid_score
from SearchSeries import exist_series, save_series_notification, update_series_notification
from SeriesService import series_exists, update_last_episode, get_series_by_name

class AddSeriesWindow(QMainWindow):
    def __init__(self, user_id):
        
        super().__init__()

        self.user_id = user_id

        # Configuation for the window
        self.setWindowTitle("Add New Series")
        self.setGeometry(800, 300, 800, 700)
        self.setStyleSheet("background-color: #191d24; color: white;")

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal vertical
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Layout horizontal for title and image
        title_layout = QHBoxLayout()

        # Image
        pixmap = QPixmap("movie.png")  
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(image_label)

        # Title
        title_label = QLabel("Add a New Series")
        title_label.setFont(QFont("Courier New", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()

        # Add title_layout to main_layout
        main_layout.addLayout(title_layout)
        
        #Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Fields for series name, IMDB link, last episode, score, snoozed
        self.series_name_input = QLineEdit()
        self.series_name_input.setPlaceholderText("Series name")
        self.series_name_input.setStyleSheet(self.input_style())
        self.series_name_input.setFixedWidth(500)
        self.series_name_input.setFixedHeight(50)
        self.series_name_input.setFont(QFont("Courier New", 12))
        main_layout.addWidget(self.series_name_input, alignment=Qt.AlignCenter)

        self.imdb_link_input = QLineEdit()
        self.imdb_link_input.setPlaceholderText("IMDB link")
        self.imdb_link_input.setStyleSheet(self.input_style())
        self.imdb_link_input.setFixedWidth(500)
        self.imdb_link_input.setFixedHeight(50)
        self.imdb_link_input.setFont(QFont("Courier New", 12))
        main_layout.addWidget(self.imdb_link_input, alignment=Qt.AlignCenter)

        self.last_episode_input = QLineEdit()
        self.last_episode_input.setPlaceholderText("Last episode watched (SXEY)")
        self.last_episode_input.setStyleSheet(self.input_style())
        self.last_episode_input.setFixedWidth(500)
        self.last_episode_input.setFixedHeight(50)
        self.last_episode_input.setFont(QFont("Courier New", 12))
        main_layout.addWidget(self.last_episode_input, alignment=Qt.AlignCenter)

        self.score_input = QLineEdit()
        self.score_input.setPlaceholderText("Score (1-10)")
        self.score_input.setStyleSheet(self.input_style())
        self.score_input.setFixedWidth(500)
        self.score_input.setFixedHeight(50)
        self.score_input.setFont(QFont("Courier New", 12))
        main_layout.addWidget(self.score_input, alignment=Qt.AlignCenter)

        self.snoozed_input = QLineEdit()
        self.snoozed_input.setPlaceholderText("Snoozed (1 or 0)")
        self.snoozed_input.setStyleSheet(self.input_style())
        self.snoozed_input.setFixedWidth(500)
        self.snoozed_input.setFixedHeight(50)
        self.snoozed_input.setFont(QFont("Courier New", 12))
        main_layout.addWidget(self.snoozed_input, alignment=Qt.AlignCenter)

        # Button for adding a new series
        add_button = QPushButton("Add")
        add_button.setStyleSheet(self.button_style())
        add_button.setFixedWidth(150)
        add_button.setFixedHeight(50)
        add_button.setFont(QFont("Courier New", 11))
        add_button.clicked.connect(self.handle_add_series)
        main_layout.addWidget(add_button, alignment=Qt.AlignCenter)

        # Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def input_style(self):
        return """
            QLineEdit {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                border-radius: 10px;
                padding: 5px;
            }
        """

    def button_style(self):
        return """
            QPushButton {
                background-color: #444;
                color: white;
                border-radius: 25px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """

    def handle_add_series(self):
        """
        Function for handling the add series button.
        """
        
        series_name = self.series_name_input.text()
        imdb_link = self.imdb_link_input.text()
        last_episode = self.last_episode_input.text()
        score_text = self.score_input.text()
        snoozed_text = self.snoozed_input.text()

        # Verify if all fields are completed
        if not series_name or not imdb_link or not last_episode or not score_text or not snoozed_text:
            QMessageBox.warning(self, "Add Series Failed", "Please complete all fields.")
            return

        # Validating IMDB link
        if not is_valid_link_imdb(imdb_link):
            QMessageBox.warning(self, "Add Series Failed", "Invalid IMDB link.")
            return

        # Validating last episode
        if not is_valid_episode_format(last_episode):
            QMessageBox.warning(self, "Add Series Failed", "Invalid episode format. Please use SXEY where X and Y are numbers.")
            return
        
        if not exist_series(imdb_link, last_episode):
            QMessageBox.warning(self, "Add Series Failed", "Series not found. Please enter a valid series.")
            return

        # Validating score
        try:
            score = float(score_text)
            if not is_valid_score(score):
                QMessageBox.warning(self, "Add Series Failed", "Invalid score. Please enter a number between 1 and 10.")
                return
        except ValueError:
            QMessageBox.warning(self, "Add Series Failed", "Invalid score. Please enter a valid number.")
            return

        # Validating snoozed
        try:
            snoozed = bool(int(snoozed_text))
            if snoozed not in [True, False]:
                QMessageBox.warning(self, "Add Series Failed", "Invalid snoozed value. Please enter 1 for True or 0 for False.")
                return
        except ValueError:
            QMessageBox.warning(self, "Add Series Failed", "Invalid snoozed value. Please enter 1 for True or 0 for False.")
            return
        
        db = next(get_db())
        
        # Check if series already exists
        if series_exists(db, self.user_id, series_name):
            reply = QMessageBox.question(self, "Series Exists", "Series already exists. Do you want to update the last watched episode?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.update_existing_series(db, series_name)
            return

        new_series = add_series(db, self.user_id, series_name, imdb_link, last_episode, score, snoozed)
        if new_series:
            QMessageBox.information(self, "Add Series", f"Series '{series_name}' added successfully!")
            save_series_notification(db, new_series.id, last_episode)
            self.close()
        else:
            QMessageBox.warning(self, "Add Series Failed", "Failed to add series.")
            
    def update_existing_series(self, db, series_name):
            """
            Function for updating an existing series.
            """
            
            # Dialog for updating last episode
            last_episode_now, ok = QInputDialog.getText(self, "Update Last Episode", "Enter new last episode (e.g., S01E01):")
            if ok:
                if is_valid_episode_format(last_episode_now):
                    series = get_series_by_name(db, self.user_id, series_name)
                    if series:
                        series_id = series.id
                        update_last_episode(db, self.user_id, series_id, last_episode_now)
                        QMessageBox.information(self, "Update Series", f"Series '{series_name}' updated successfully!")
                        update_series_notification(db, series_id, last_episode_now)
                        self.close()
                    else:
                        QMessageBox.warning(self, "Update Failed", "Series not found.")
                else:
                    QMessageBox.warning(self, "Update Failed", "Invalid episode format. Please use SXEY where X and Y are numbers.")



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = AddSeriesWindow(user_id=1) 
#     window.show()
#     sys.exit(app.exec_())