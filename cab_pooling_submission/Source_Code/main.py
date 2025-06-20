import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from database.db_manager import DatabaseManager
from controllers.auth import AuthController
from controllers.trip import TripController
from controllers.search import SearchController
from ui.auth_window import AuthWindow

def main():
    # Initialize application
    app = QApplication(sys.argv)
    
    # Initialize database and controllers
    db_manager = DatabaseManager()
    auth_controller = AuthController(db_manager)
    trip_controller = TripController(db_manager)
    search_controller = SearchController(db_manager)
    
    # Show authentication window
    auth_window = AuthWindow(auth_controller, trip_controller, search_controller)
    auth_window.show()
    
    # Run the application loop
    sys.exit(app.exec_())

def join_trip(self, trip_id):
    seats_booked = 1  # Assuming the user books one seat
    success, message = self.trip_controller.add_participant(trip_id, self.user_data['id'], seats_booked)
    
    if success:
        QMessageBox.information(self, "Success", "You have joined the trip!")
        # Optionally, show contact information of the trip creator
    else:
        QMessageBox.warning(self, "Error", message)

if __name__ == "__main__":
    main()
