import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from interface.AddWindow import AddSeriesWindow
from interface.ViewWindow import ViewSeriesWindow
from interface.NotificationsWindow import ViewNotificationsWindow

class MainWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id

        # Configuartion for the window
        self.setWindowTitle("Series Manager - Main")
        self.setGeometry(700, 300, 1000, 700)
        self.setStyleSheet("background-color: #191d24; color: white;")

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout for the main window vertical
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Layout horizontal for title and image
        top_layout = QHBoxLayout()

        # Image
        pixmap = QPixmap("images/icon.png") 
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignLeft)
        top_layout.addWidget(image_label)

        # Title
        title_label = QLabel("Binge Watch")
        title_label.setFont(QFont("Courier New", 25, QFont.Bold))
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        top_layout.addWidget(title_label)

        # Spacer
        top_layout.addStretch()

        # Add top_layout to main_layout
        main_layout.addLayout(top_layout)

        # Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Layout orizontal for the text and image above the "Add a New Series" button
        add_series_layout = QHBoxLayout()

        # Image for the "Add a New Series" section
        add_series_pixmap = QPixmap("images/add.png") 
        add_series_image_label = QLabel()
        add_series_image_label.setPixmap(add_series_pixmap)
        add_series_image_label.setAlignment(Qt.AlignLeft)
        add_series_layout.addWidget(add_series_image_label)

        # Text above the "Add a New Series" button
        add_series_label = QLabel("Add a New Series  ")
        add_series_label.setFont(QFont("Courier New", 20, QFont.Bold))
        add_series_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        add_series_layout.addWidget(add_series_label)
        add_series_layout.addStretch()

        # Add add_series_layout to main_layout
        main_layout.addLayout(add_series_layout)

        # Button for adding a new series
        add_series_button = QPushButton("Add")
        add_series_button.setStyleSheet(self.button_style())
        add_series_button.setFixedWidth(200)
        add_series_button.setFixedHeight(50)
        add_series_button.setFont(QFont("Courier New", 14))
        add_series_button.clicked.connect(self.open_add_series_window)
        add_series_layout.addWidget(add_series_button, alignment=Qt.AlignLeft)
        add_series_layout.addStretch()

        # Layout orizontal for the text and image above the "View Your Series" button
        view_series_layout = QHBoxLayout()

        # Image for the "View Your Series" section
        view_series_pixmap = QPixmap("images/list.png") 
        view_series_image_label = QLabel()
        view_series_image_label.setPixmap(view_series_pixmap)
        view_series_image_label.setAlignment(Qt.AlignLeft)
        view_series_layout.addWidget(view_series_image_label)

        # Text above the "View Your Series" button
        view_series_label = QLabel("View Your Series  ")
        view_series_label.setFont(QFont("Courier New", 20, QFont.Bold))
        view_series_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        view_series_layout.addWidget(view_series_label)
        view_series_layout.addStretch()

        # Add view_series_layout to main_layout
        main_layout.addLayout(view_series_layout)

        # Button for viewing the user's series
        view_series_button = QPushButton("View")
        view_series_button.setStyleSheet(self.button_style())
        view_series_button.setFixedWidth(200)
        view_series_button.setFixedHeight(50)
        view_series_button.setFont(QFont("Courier New", 14))
        view_series_button.clicked.connect(self.open_view_series_window)
        view_series_layout.addWidget(view_series_button, alignment=Qt.AlignLeft)
        view_series_layout.addStretch()

        # Layout orizontal for the text and image above the "View Notifications" button
        view_notifications_layout = QHBoxLayout()

        # Image for the "View Notifications" section
        view_notifications_pixmap = QPixmap("images/notify.png") 
        view_notifications_image_label = QLabel()
        view_notifications_image_label.setPixmap(view_notifications_pixmap)
        view_notifications_image_label.setAlignment(Qt.AlignLeft)
        view_notifications_layout.addWidget(view_notifications_image_label)

        # Text above the "View Notifications" button
        view_notifications_label = QLabel("View Notifications")
        view_notifications_label.setFont(QFont("Courier New", 20, QFont.Bold))
        view_notifications_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        view_notifications_layout.addWidget(view_notifications_label)
        view_notifications_layout.addStretch()

        # Add view_notifications_layout to main_layout
        main_layout.addLayout(view_notifications_layout)

        # Button for viewing the user's notifications
        view_notifications_button = QPushButton("View")
        view_notifications_button.setStyleSheet(self.button_style())
        view_notifications_button.setFixedWidth(200)
        view_notifications_button.setFixedHeight(50)
        view_notifications_button.setFont(QFont("Courier New", 14))
        view_notifications_button.clicked.connect(self.open_view_notifications_window)
        view_notifications_layout.addWidget(view_notifications_button, alignment=Qt.AlignLeft)
        view_notifications_layout.addStretch()

        # Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Layout for the logout button
        logout_layout = QHBoxLayout()
        logout_layout.addStretch()  
        
        # Button for logging out
        logout_button = QPushButton("Logout")
        logout_button.setStyleSheet(self.button_style())
        logout_button.setFixedWidth(200)
        logout_button.setFixedHeight(50)
        logout_button.setFont(QFont("Courier New", 14))
        logout_button.clicked.connect(self.logout)
        logout_layout.addWidget(logout_button, alignment=Qt.AlignRight)

        # Add logout_layout to main_layout
        main_layout.addLayout(logout_layout)

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
        
    # Funtions for opening the windows
    def open_add_series_window(self):
        self.add_series_window = AddSeriesWindow(self.user_id)
        self.add_series_window.show()

    def open_view_series_window(self):
        self.view_series_window = ViewSeriesWindow(self.user_id)
        self.view_series_window.show()

    def open_view_notifications_window(self):
        self.view_notifications_window = ViewNotificationsWindow(self.user_id)
        self.view_notifications_window.show()

    def logout(self):
        self.close()  

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow(user_id=1)  
#     window.show()
#     sys.exit(app.exec_())