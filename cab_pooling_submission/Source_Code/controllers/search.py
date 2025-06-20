from Levenshtein import distance as levenshtein_distance

class SearchController:
    def __init__(self, db_manager):
        self.db_manager = db_manager  # Store database connection

    def fuzzy_search(self, query):
        """Search trips with fuzzy matching and return results"""
        trips = self.db_manager.get_all_trips()  # Fetch trips from the database
        matches = []
        
        # Fuzzy search logic
        for trip in trips:
            source_dist = levenshtein_distance(query.lower(), trip['source'].lower())
            dest_dist = levenshtein_distance(query.lower(), trip['destination'].lower())
            
            if source_dist <= 2 or dest_dist <= 2:
                matches.append(trip)
        
        return matches

    def search_trips(self, source, destination, date):
        cursor = self.db_manager.conn.cursor()
        cursor.execute('''
            SELECT t.*, u.username as creator_name 
            FROM trips t 
            JOIN users u ON t.creator_id = u.id 
            WHERE t.source LIKE ? 
            AND t.destination LIKE ? 
            AND t.date = ? 
            AND t.seats_available > 0
            ORDER BY t.time
        ''', (f'%{source}%', f'%{destination}%', date))
        return cursor.fetchall()

    def search_trips_by_date_range(self, source, destination, start_date, end_date):
        cursor = self.db_manager.conn.cursor()
        cursor.execute('''
            SELECT t.*, u.username as creator_name 
            FROM trips t 
            JOIN users u ON t.creator_id = u.id 
            WHERE t.source LIKE ? 
            AND t.destination LIKE ? 
            AND t.date BETWEEN ? AND ?
            AND t.seats_available > 0
            ORDER BY t.date, t.time
        ''', (f'%{source}%', f'%{destination}%', start_date, end_date))
        return cursor.fetchall()

    def get_popular_routes(self):
        cursor = self.db_manager.conn.cursor()
        cursor.execute('''
            SELECT source, destination, COUNT(*) as trip_count
            FROM trips
            GROUP BY source, destination
            ORDER BY trip_count DESC
            LIMIT 5
        ''')
        return cursor.fetchall()

    def get_available_trips_for_user(self, user_id, source, destination, date):
        cursor = self.db_manager.conn.cursor()
        cursor.execute('''
            SELECT t.*, u.username as creator_name 
            FROM trips t 
            JOIN users u ON t.creator_id = u.id 
            WHERE t.source LIKE ? 
            AND t.destination LIKE ? 
            AND t.date = ? 
            AND t.seats_available > 0
            AND t.creator_id != ?
            ORDER BY t.time
        ''', (f'%{source}%', f'%{destination}%', date, user_id))
        return cursor.fetchall()
