import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QMessageBox, QInputDialog, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from database.Connection import get_db
from database.Models import Series
from SeriesService import delete_series, update_score, snooze_unsnooze_series
from Validation import is_valid_score

class ViewSeriesWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id

        # Configuration for the window
        self.setWindowTitle("View Your Series")
        self.setGeometry(400, 300, 1500, 600)
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
        pixmap = QPixmap("movie.png")  # Înlocuiește cu calea către imaginea ta
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(image_label)

        # Title
        title_label = QLabel("Your Series")
        title_label.setFont(QFont("Comic Sans MS", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()

        # Add title_layout to main_layout
        main_layout.addLayout(title_layout)

        #Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Table for the series
        self.series_table = QTableWidget()
        self.series_table.setColumnCount(6)
        self.series_table.setStyleSheet("background-color: #3c4554; color: black;")
        self.series_table.setHorizontalHeaderLabels(["Series Name", "Last Episode", "Score", "Snoozed", "", ""])
        self.series_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.series_table)
        
        self.series_table.setStyleSheet("""
            QHeaderView::section {
                background-color: #3c4554;
                color: black;
            }
        """)

        # Load user series
        self.load_user_series()

    def load_user_series(self):
        """
        function to load all series for the user
        """
        
        db = next(get_db())
        series_list = db.query(Series).filter(Series.user_id == self.user_id).all()

        self.series_table.setRowCount(len(series_list))
        for row, series in enumerate(series_list):
            self.series_table.setItem(row, 0, QTableWidgetItem(series.name))
            self.series_table.setItem(row, 1, QTableWidgetItem(series.last_episode))
            self.series_table.setItem(row, 2, QTableWidgetItem(str(series.score)))
            self.series_table.setItem(row, 3, QTableWidgetItem("Snoozed" if series.snoozed else "Unsnoozed"))

            # Buton pentru ștergerea serialului
            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet(self.button_style())
            delete_button.clicked.connect(lambda _, s=series: self.handle_delete_series(s))
            self.series_table.setCellWidget(row, 4, delete_button)

            # Buton pentru actualizarea scorului și snoozed
            update_button = QPushButton("Update")
            update_button.setStyleSheet(self.button_style())
            update_button.clicked.connect(lambda _, s=series: self.handle_update_series(s))
            self.series_table.setCellWidget(row, 5, update_button)

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

    def handle_delete_series(self, series):
        """Funtion to delete a series."""
        
        db = next(get_db())
        if delete_series(db, self.user_id, series.name):
            QMessageBox.information(self, "Delete Series", f"Series '{series.name}' deleted successfully!")
            self.load_user_series()  # Reload user series
        else:
            QMessageBox.warning(self, "Delete Series Failed", "Failed to delete series.")

    def handle_update_series(self, series):
            """Function to update a series."""
            
            valid_score = False
            db = next(get_db())
            while not valid_score:
                new_score, ok = QInputDialog.getDouble(self, "Update Score", "Enter new score (1-10):", decimals=1)
                if ok:
                    if is_valid_score(new_score):
                        valid_score = True
                        update_score(db, self.user_id, series.name, new_score)
                    else:
                        QMessageBox.warning(self, "Update Score Failed", "Invalid score. Please enter a number between 1 and 10.")
                else:
                    break

            # verify if the series is snoozed to update it
            if series.snoozed:
                reply = QMessageBox.question(self, "Confirm Unsnooze", "Series is currently snoozed. Do you want to unsnooze it?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    snooze_unsnooze_series(db, self.user_id, series.id)
            else:
                reply = QMessageBox.question(self, "Confirm Snooze", "Series is currently unsnoozed. Do you want to snooze it?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    snooze_unsnooze_series(db, self.user_id, series.id)

            QMessageBox.information(self, "Update Series", f"Series '{series.name}' updated successfully!")
            self.load_user_series()  # Reload user series


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ViewSeriesWindow(user_id=1) 
#     window.show()
#     sys.exit(app.exec_())