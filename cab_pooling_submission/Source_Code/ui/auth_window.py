from PyQt5.QtWidgets import (QWidget, QMessageBox, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QLineEdit, QLabel, QGridLayout)
from PyQt5.QtCore import Qt

class AuthWindow(QWidget):
    def __init__(self, auth_controller, trip_controller, search_controller):
        super().__init__()
        
        # Store controllers for later use
        self.auth_controller = auth_controller
        self.trip_controller = trip_controller
        self.search_controller = search_controller
        
        # Initialize UI components
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Cab Pooling - Login")
        self.setGeometry(300, 300, 400, 300)
        
        # Create main layout
        layout = QGridLayout()
        self.setLayout(layout)
        
        # Create input fields
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        # Create buttons
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px;")
        
        self.signup_button = QPushButton("Sign Up")
        self.signup_button.clicked.connect(self.show_signup)
        self.signup_button.setStyleSheet("background-color: #2196F3; color: white; padding: 5px;")
        
        # Add widgets to layout
        layout.addWidget(self.username_label, 0, 0)
        layout.addWidget(self.username_input, 0, 1)
        layout.addWidget(self.password_label, 1, 0)
        layout.addWidget(self.password_input, 1, 1)
        
        # Add buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.signup_button)
        layout.addLayout(button_layout, 2, 0, 1, 2)
        
        # Center the window
        self.center()
        
    def center(self):
        # Center window on screen
        frame_geometry = self.frameGeometry()
        screen_center = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        
        success, message = self.auth_controller.login_user(username, password)
        if success:
            QMessageBox.information(self, "Success", "Login successful!")
            # Open main application window
            from ui.main_window import MainWindow
            self.main_window = MainWindow(self.auth_controller, self.trip_controller, 
                                        self.search_controller, message)  # message contains user data
            self.main_window.show()
            self.close()  # Close login window
        else:
            QMessageBox.warning(self, "Error", message)
    
    def show_signup(self):
        self.signup_window = SignupWindow(self.auth_controller)
        self.signup_window.show()

class SignupWindow(QWidget):
    def __init__(self, auth_controller):
        super().__init__()
        self.auth_controller = auth_controller
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Cab Pooling - Sign Up")
        self.setGeometry(350, 350, 400, 300)
        
        layout = QGridLayout()
        self.setLayout(layout)
        
        # Create input fields
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username")
        
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Choose a password")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        
        self.phone_label = QLabel("Phone:")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter your phone number")
        
        self.signup_button = QPushButton("Create Account")
        self.signup_button.clicked.connect(self.handle_signup)
        self.signup_button.setStyleSheet("background-color: #2196F3; color: white; padding: 5px;")
        
        # Add widgets to layout
        layout.addWidget(self.username_label, 0, 0)
        layout.addWidget(self.username_input, 0, 1)
        layout.addWidget(self.password_label, 1, 0)
        layout.addWidget(self.password_input, 1, 1)
        layout.addWidget(self.email_label, 2, 0)
        layout.addWidget(self.email_input, 2, 1)
        layout.addWidget(self.phone_label, 3, 0)
        layout.addWidget(self.phone_input, 3, 1)
        layout.addWidget(self.signup_button, 4, 0, 1, 2)
        
        self.center()
        
    def center(self):
        frame_geometry = self.frameGeometry()
        screen_center = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
        
    def handle_signup(self):
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and password are required")
            return
            
        success, message = self.auth_controller.register_user(username, password, email, phone)
        if success:
            QMessageBox.information(self, "Success", "Account created successfully! You can now login.")
            self.close()
        else:
            QMessageBox.warning(self, "Error", message)
