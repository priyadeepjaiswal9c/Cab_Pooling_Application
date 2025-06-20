class TripController:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_trip(self, creator_id, source, destination, date, time, vehicle_type, seats_total):
        cursor = self.db_manager.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO trips (
                    creator_id, source, destination, date, time,
                    vehicle_type, seats_total, seats_available
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (creator_id, source, destination, date, time, vehicle_type, seats_total, seats_total))
            self.db_manager.conn.commit()
            return True, "Trip created successfully"
        except Exception as e:
            return False, f"Error creating trip: {str(e)}"

    def get_user_trips(self, user_id):
        cursor = self.db_manager.conn.cursor()
        # Get created trips
        cursor.execute('''
            SELECT t.*, 'creator' as role 
            FROM trips t 
            WHERE creator_id = ? 
            ORDER BY date, time
        ''', (user_id,))
        created_trips = cursor.fetchall()
        
        # Get joined trips
        cursor.execute('''
            SELECT t.*, 'participant' as role 
            FROM trips t 
            JOIN trip_participants tp ON t.id = tp.trip_id 
            WHERE tp.user_id = ? 
            ORDER BY date, time
        ''', (user_id,))
        joined_trips = cursor.fetchall()
        
        return created_trips + joined_trips

    def get_trip_details(self, trip_id):
        cursor = self.db_manager.conn.cursor()
        cursor.execute('''
            SELECT t.*, u.username as creator_name 
            FROM trips t 
            JOIN users u ON t.creator_id = u.id 
            WHERE t.id = ?
        ''', (trip_id,))
        return cursor.fetchone()

    def update_seats_available(self, trip_id, seats_booked):
        cursor = self.db_manager.conn.cursor()
        try:
            cursor.execute('''
                UPDATE trips 
                SET seats_available = seats_available - ? 
                WHERE id = ? AND seats_available >= ?
            ''', (seats_booked, trip_id, seats_booked))
            self.db_manager.conn.commit()
            return True, "Seats updated successfully"
        except Exception as e:
            return False, f"Error updating seats: {str(e)}"

    def add_participant(self, trip_id, user_id, seats_booked):
        cursor = self.db_manager.conn.cursor()
        try:
            # First update available seats
            success, message = self.update_seats_available(trip_id, seats_booked)
            if not success:
                return False, message

            # Then add participant
            cursor.execute('''
                INSERT INTO trip_participants (trip_id, user_id, seats_booked)
                VALUES (?, ?, ?)
            ''', (trip_id, user_id, seats_booked))
            self.db_manager.conn.commit()
            return True, "Successfully joined the trip"
        except Exception as e:
            return False, f"Error joining trip: {str(e)}"

    def get_trip_participants(self, trip_id):
        cursor = self.db_manager.conn.cursor()
        cursor.execute('''
            SELECT tp.*, u.username 
            FROM trip_participants tp 
            JOIN users u ON tp.user_id = u.id 
            WHERE tp.trip_id = ?
        ''', (trip_id,))
        return cursor.fetchall()

    def delete_trip(self, trip_id):
        cursor = self.db_manager.conn.cursor()
        try:
            # First delete all participants
            cursor.execute('DELETE FROM trip_participants WHERE trip_id = ?', (trip_id,))
            # Then delete the trip
            cursor.execute('DELETE FROM trips WHERE id = ?', (trip_id,))
            self.db_manager.conn.commit()
            return True, "Trip deleted successfully"
        except Exception as e:
            return False, f"Error deleting trip: {str(e)}"

