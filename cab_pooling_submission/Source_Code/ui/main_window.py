from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QTabWidget, QMessageBox, QLineEdit, QComboBox,
                            QDateEdit, QTimeEdit, QSpinBox, QGridLayout, QScrollArea)
from PyQt5.QtCore import Qt, QDate, QTime
from datetime import datetime

class MainWindow(QWidget):
    def __init__(self, auth_controller, trip_controller, search_controller, user_data):
        super().__init__()
        self.auth_controller = auth_controller
        self.trip_controller = trip_controller
        self.search_controller = search_controller
        self.user_data = user_data
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Cab Pooling - Main")
        self.setGeometry(100, 100, 800, 600)
        
        # Create main layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Create header with user info and logout button
        header_layout = QHBoxLayout()
        welcome_label = QLabel(f"Welcome, {self.user_data['username']}!")
        welcome_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(self.handle_logout)
        logout_button.setStyleSheet("background-color: #f44336; color: white; padding: 5px;")
        
        header_layout.addWidget(welcome_label)
        header_layout.addStretch()
        header_layout.addWidget(logout_button)
        layout.addLayout(header_layout)
        
        # Create tab widget for different sections
        tabs = QTabWidget()
        
        # Create tabs
        create_trip_tab = self.create_trip_tab()
        search_trip_tab = self.search_trip_tab()
        my_trips_tab = self.my_trips_tab()
        
        # Add tabs to widget
        tabs.addTab(create_trip_tab, "Create Trip")
        tabs.addTab(search_trip_tab, "Search Trips")
        tabs.addTab(my_trips_tab, "My Trips")
        
        layout.addWidget(tabs)
        
        # Center the window
        self.center()
        
    def center(self):
        frame_geometry = self.frameGeometry()
        screen_center = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
        
    def create_trip_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Create scroll area for the form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        form_layout = QGridLayout()
        scroll_content.setLayout(form_layout)
        
        # Create form fields
        # Source
        form_layout.addWidget(QLabel("Source:"), 0, 0)
        self.source_input = QLineEdit()
        self.source_input.setPlaceholderText("Enter source location")
        form_layout.addWidget(self.source_input, 0, 1)
        
        # Destination
        form_layout.addWidget(QLabel("Destination:"), 1, 0)
        self.destination_input = QLineEdit()
        self.destination_input.setPlaceholderText("Enter destination location")
        form_layout.addWidget(self.destination_input, 1, 1)
        
        # Date
        form_layout.addWidget(QLabel("Date:"), 2, 0)
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        form_layout.addWidget(self.date_input, 2, 1)
        
        # Time
        form_layout.addWidget(QLabel("Time:"), 3, 0)
        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime.currentTime())
        form_layout.addWidget(self.time_input, 3, 1)
        
        # Vehicle Type
        form_layout.addWidget(QLabel("Vehicle Type:"), 4, 0)
        self.vehicle_type = QComboBox()
        self.vehicle_type.addItems(["Car", "SUV", "Van", "Bus"])
        form_layout.addWidget(self.vehicle_type, 4, 1)
        
        # Total Seats
        form_layout.addWidget(QLabel("Total Seats:"), 5, 0)
        self.seats_input = QSpinBox()
        self.seats_input.setRange(1, 50)
        self.seats_input.setValue(4)
        form_layout.addWidget(self.seats_input, 5, 1)
        
        # Create Trip Button
        create_button = QPushButton("Create Trip")
        create_button.clicked.connect(self.handle_create_trip)
        create_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        form_layout.addWidget(create_button, 6, 0, 1, 2)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        return tab
        
    def search_trip_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Create search form
        form_layout = QGridLayout()
        
        # Source
        form_layout.addWidget(QLabel("From:"), 0, 0)
        self.search_source = QLineEdit()
        self.search_source.setPlaceholderText("Enter source location")
        form_layout.addWidget(self.search_source, 0, 1)
        
        # Destination
        form_layout.addWidget(QLabel("To:"), 1, 0)
        self.search_destination = QLineEdit()
        self.search_destination.setPlaceholderText("Enter destination location")
        form_layout.addWidget(self.search_destination, 1, 1)
        
        # Date
        form_layout.addWidget(QLabel("Date:"), 2, 0)
        self.search_date = QDateEdit()
        self.search_date.setDate(QDate.currentDate())
        self.search_date.setCalendarPopup(True)
        form_layout.addWidget(self.search_date, 2, 1)
        
        # Search Button
        search_button = QPushButton("Search Trips")
        search_button.clicked.connect(self.handle_search_trips)
        search_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        form_layout.addWidget(search_button, 3, 0, 1, 2)
        
        # Results area with scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.search_results_container = QWidget()
        self.search_results_layout = QVBoxLayout()
        self.search_results_container.setLayout(self.search_results_layout)
        scroll.setWidget(self.search_results_container)
        
        layout.addLayout(form_layout)
        layout.addWidget(scroll)
        return tab
        
    def my_trips_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Add refresh button
        refresh_button = QPushButton("Refresh My Trips")
        refresh_button.clicked.connect(self.handle_refresh_trips)
        refresh_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        layout.addWidget(refresh_button)
        
        # Trips display area with scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.trips_container = QWidget()
        self.trips_layout = QVBoxLayout()
        self.trips_container.setLayout(self.trips_layout)
        scroll.setWidget(self.trips_container)
        
        layout.addWidget(scroll)
        return tab
        
    def handle_logout(self):
        reply = QMessageBox.question(self, 'Logout', 'Are you sure you want to logout?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.close()  # Close main window
            # Show login window again
            from ui.auth_window import AuthWindow
            self.login_window = AuthWindow(self.auth_controller, self.trip_controller, self.search_controller)
            self.login_window.show()
            
    def handle_create_trip(self):
        # Get values from form
        source = self.source_input.text()
        destination = self.destination_input.text()
        date = self.date_input.date().toString("yyyy-MM-dd")
        time = self.time_input.time().toString("HH:mm")
        vehicle_type = self.vehicle_type.currentText()
        seats = self.seats_input.value()
        
        # Validate inputs
        if not source or not destination:
            QMessageBox.warning(self, "Error", "Please enter both source and destination")
            return
            
        # Create trip using controller
        success, message = self.trip_controller.create_trip(
            self.user_data['id'],
            source,
            destination,
            date,
            time,
            vehicle_type,
            seats
        )
        
        if success:
            QMessageBox.information(self, "Success", "Trip created successfully!")
            # Clear form
            self.source_input.clear()
            self.destination_input.clear()
            self.date_input.setDate(QDate.currentDate())
            self.time_input.setTime(QTime.currentTime())
            self.vehicle_type.setCurrentIndex(0)
            self.seats_input.setValue(4)
        else:
            QMessageBox.warning(self, "Error", message)
            
    def handle_search_trips(self):
        # Get search parameters
        source = self.search_source.text()
        destination = self.search_destination.text()
        date = self.search_date.date().toString("yyyy-MM-dd")
        
        # Validate inputs
        if not source or not destination:
            QMessageBox.warning(self, "Error", "Please enter both source and destination")
            return
            
        # Clear previous results
        for i in reversed(range(self.search_results_layout.count())): 
            self.search_results_layout.itemAt(i).widget().setParent(None)
            
        # Search trips using controller
        trips = self.search_controller.search_trips(source, destination, date)
        
        if trips:
            # Create a widget for each trip
            for trip in trips:
                trip_widget = QWidget()
                trip_layout = QVBoxLayout()
                trip_widget.setLayout(trip_layout)
                
                # Trip details
                details = QLabel(
                    f"From: {trip['source']}\n"
                    f"To: {trip['destination']}\n"
                    f"Date: {trip['date']}\n"
                    f"Time: {trip['time']}\n"
                    f"Vehicle: {trip['vehicle_type']}\n"
                    f"Available Seats: {trip['seats_available']}\n"
                    f"Created by: {trip['creator_name']}"
                )
                trip_layout.addWidget(details)
                
                # Join button
                join_button = QPushButton("Join Trip")
                join_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px;")
                join_button.clicked.connect(lambda checked, t=trip: self.handle_join_trip(t))
                trip_layout.addWidget(join_button)
                
                # Add separator
                separator = QLabel("-------------------")
                separator.setAlignment(Qt.AlignCenter)
                trip_layout.addWidget(separator)
                
                self.search_results_layout.addWidget(trip_widget)
        else:
            no_results = QLabel("No trips found matching your criteria.")
            no_results.setAlignment(Qt.AlignCenter)
            self.search_results_layout.addWidget(no_results)
            
    def handle_join_trip(self, trip):
        # Check if user is trying to join their own trip
        if trip['creator_id'] == self.user_data['id']:
            QMessageBox.warning(self, "Error", "You cannot join your own trip!")
            return
            
        # Show confirmation dialog
        reply = QMessageBox.question(
            self, 
            'Join Trip', 
            f'Are you sure you want to join this trip from {trip["source"]} to {trip["destination"]}?',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Join the trip
            success, message = self.trip_controller.add_participant(
                trip['id'],
                self.user_data['id'],
                1  # Assuming booking one seat
            )
            
            if success:
                QMessageBox.information(self, "Success", "You have successfully joined the trip!")
                # Show creator's contact info
                creator_info = self.auth_controller.get_user_contact(trip['creator_id'])
                if creator_info:
                    QMessageBox.information(
                        self,
                        "Trip Creator Contact",
                        f"Contact the trip creator:\n"
                        f"Username: {creator_info['username']}\n"
                        f"Email: {creator_info['email']}\n"
                        f"Phone: {creator_info['phone']}"
                    )
                # Refresh search results and my trips
                self.handle_search_trips()
                self.handle_refresh_trips()
            else:
                QMessageBox.warning(self, "Error", message)
            
    def handle_refresh_trips(self):
        # Get user's trips using controller
        trips = self.trip_controller.get_user_trips(self.user_data['id'])
        
        # Clear previous trips display
        for i in reversed(range(self.trips_layout.count())):
            self.trips_layout.itemAt(i).widget().setParent(None)
        
        if trips:
            for trip in trips:
                trip_widget = QWidget()
                trip_layout = QVBoxLayout()
                trip_widget.setLayout(trip_layout)
                
                # Trip details
                role_text = "You created this trip" if trip['role'] == 'creator' else "You joined this trip"
                details = QLabel(
                    f"{role_text}:\n"
                    f"From: {trip['source']}\n"
                    f"To: {trip['destination']}\n"
                    f"Date: {trip['date']}\n"
                    f"Time: {trip['time']}\n"
                    f"Vehicle: {trip['vehicle_type']}\n"
                    f"Total Seats: {trip['seats_total']}\n"
                    f"Available Seats: {trip['seats_available']}\n"
                )
                trip_layout.addWidget(details)
                
                # Delete button (only for created trips)
                if trip['role'] == 'creator':
                    delete_button = QPushButton("Delete Trip")
                    delete_button.setStyleSheet("background-color: #f44336; color: white; padding: 5px;")
                    delete_button.clicked.connect(lambda checked, t=trip: self.handle_delete_trip(t['id']))
                    trip_layout.addWidget(delete_button)
                
                # Add separator
                separator = QLabel("-------------------")
                separator.setAlignment(Qt.AlignCenter)
                trip_layout.addWidget(separator)
                
                self.trips_layout.addWidget(trip_widget)
        else:
            no_trips = QLabel("You haven't created or joined any trips yet.")
            no_trips.setAlignment(Qt.AlignCenter)
            self.trips_layout.addWidget(no_trips)
            
    def handle_delete_trip(self, trip_id):
        # Show confirmation dialog
        reply = QMessageBox.question(
            self,
            'Delete Trip',
            'Are you sure you want to delete this trip?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.trip_controller.delete_trip(trip_id)
            if success:
                QMessageBox.information(self, "Success", "Trip deleted successfully!")
                self.handle_refresh_trips()  # Refresh the trips display
            else:
                QMessageBox.warning(self, "Error", message)
