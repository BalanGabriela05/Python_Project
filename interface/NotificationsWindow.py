import sys
import webbrowser
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from database.Connection import get_db
from NotificationsService import all_notifications

class ViewNotificationsWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id

        # Configuration for the window
        self.setWindowTitle("View Notifications")
        self.setGeometry(600, 300, 850, 650)
        self.setStyleSheet("background-color: #191d24; color: white;")
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal vertical
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Layout orizontal for title and image
        title_layout = QHBoxLayout()

        # Image
        pixmap = QPixmap("images/movie.png") 
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(image_label)

        # Title
        title_label = QLabel("Notifications")
        title_label.setFont(QFont("Comic Sans MS", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()

        # Add title_layout to main_layout
        main_layout.addLayout(title_layout)
        
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))  

        # Load notifications
        self.load_notifications(main_layout)

    def load_notifications(self, main_layout):
        """ Load all notifications for the user """
        
        db = next(get_db())
        notifications = all_notifications(db, self.user_id)

        for notification in notifications:
            series_name = notification.series.name
            new_episode = notification.new_episode
            notification_date = notification.notification_date.strftime("%Y-%m-%d") if notification.notification_date else "N/A"
            youtube_link = notification.youtube_trailer

            # Layout for each notification
            notification_layout = QVBoxLayout()

            # Title for the series
            series_label = QLabel(f"Series: {series_name}")
            series_label.setFont(QFont("Courier New", 16, QFont.Bold))
            notification_layout.addWidget(series_label)

            # New episode
            episode_label = QLabel(f"!New Episode: {new_episode}")
            episode_label.setFont(QFont("Courier New", 14))
            notification_layout.addWidget(episode_label)

            # Date of the episode
            date_label = QLabel(f"Date: {notification_date}")
            date_label.setFont(QFont("Courier New", 14))
            notification_layout.addWidget(date_label)

            # Link YouTube
            if youtube_link != "No trailer found.":
                # the layout for the button 
                button_layout = QHBoxLayout()

                # Image for the YouTube button
                button_pixmap = QPixmap("images/youtube.png") 
                button_image_label = QLabel()
                button_image_label.setPixmap(button_pixmap)
                button_image_label.setAlignment(Qt.AlignCenter)
                button_layout.addWidget(button_image_label)

                # Button YouTube
                youtube_button = QPushButton("Watch Trailer")
                youtube_button.setFont(QFont("Courier New", 14))
                youtube_button.setStyleSheet(self.button_style())
                youtube_button.setFixedWidth(400)
                youtube_button.clicked.connect(lambda _, link=youtube_link: webbrowser.open(link))
                button_layout.addWidget(youtube_button)
                button_layout.addStretch()

                # Add button_layout to notification_layout
                notification_layout.addLayout(button_layout)

                main_layout.addLayout(notification_layout)
            
            else:
                youtube_label = QLabel("No trailer available.")
                youtube_label.setFont(QFont("Courier New", 14))
                notification_layout.addWidget(youtube_label)
            
            s_label = QLabel(f"---")
            s_label.setFont(QFont("Courier New", 16, QFont.Bold))
            s_label.setAlignment(Qt.AlignCenter)
            notification_layout.addWidget(s_label)

            main_layout.addLayout(notification_layout)

            main_layout.addSpacing(20)

    def button_style(self):
        return """
            QPushButton {
                background-color: #444;
                color: white;
                border-radius: 15px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """
    
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ViewNotificationsWindow(user_id=1)  
#     window.show()
#     sys.exit(app.exec_())