import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from sqlalchemy.orm import sessionmaker
from database.Models import User
from database.Connection import get_db
from UserService import login, sign_up
from MainWindow import MainWindow  # Importă noua fereastră

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # configuration for the window
        self.setWindowTitle("Login - Series Manager")
        self.setGeometry(800, 300, 800, 600)
        self.setStyleSheet("background-color: #191d24; color: white;")

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal vertical
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Layout orizontal for title and image
        top_layout = QHBoxLayout()

        # for the image
        pixmap = QPixmap("icon.png")
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

        # Layout vertical for buttons and inputs
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet(self.input_style())
        self.username_input.setFixedWidth(400)
        self.username_input.setFixedHeight(70)
        self.username_input.setFont(QFont("Courier New", 12))
        form_layout.addWidget(self.username_input)

        # Space between elements
        form_layout.addSpacing(10)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.input_style())
        self.password_input.setFixedWidth(400)
        self.password_input.setFixedHeight(70)
        self.password_input.setFont(QFont("Courier New", 12))
        form_layout.addWidget(self.password_input)

        # Space between elements
        form_layout.addSpacing(20)

        # Button Login
        login_button = QPushButton("Login")
        login_button.setStyleSheet(self.button_style())
        login_button.setFixedWidth(150)
        login_button.setFixedHeight(60)
        login_button.setFont(QFont("Courier New", 11))
        login_button.clicked.connect(self.handle_login)
        form_layout.addWidget(login_button, alignment=Qt.AlignCenter)

        # Space between elements
        form_layout.addSpacing(10)

        # Button Sign Up
        signup_button = QPushButton("Sign Up")
        signup_button.setStyleSheet(self.button_style())
        signup_button.setFixedWidth(150)
        signup_button.setFixedHeight(60)
        signup_button.setFont(QFont("Courier New", 11))
        signup_button.clicked.connect(self.handle_signup)
        form_layout.addWidget(signup_button, alignment=Qt.AlignCenter)

        # Add form_layout to main_layout
        main_layout.addLayout(form_layout)

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

    def handle_login(self):
        """Function for login."""
        username = self.username_input.text()
        password = self.password_input.text()
        db = next(get_db())

        if login(username, password, db):
            user_id = db.query(User).filter(User.username == username).first().user_id
            self.main_window = MainWindow(user_id)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def handle_signup(self):
        """Function for sign up."""
        username = self.username_input.text()
        password = self.password_input.text()
        db = next(get_db())

        if sign_up(username, password, db):
            user_id = db.query(User).filter(User.username == username).first().user_id
            self.main_window = MainWindow(user_id)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Sign Up Failed", "Username already exists.")

def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()