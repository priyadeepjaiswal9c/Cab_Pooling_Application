class Trip:
    def __init__(self, id, creator_id, source, destination, date, time, vehicle_type, seats_total, seats_available):
        self.id = id
        self.creator_id = creator_id
        self.source = source
        self.destination = destination
        self.date = date
        self.time = time
        self.vehicle_type = vehicle_type
        self.seats_total = seats_total
        self.seats_available = seats_available

    @staticmethod
    def from_row(row):
        return Trip(
            row['id'], row['creator_id'], row['source'], row['destination'],
            row['date'], row['time'], row['vehicle_type'],
            row['seats_total'], row['seats_available']
        )
