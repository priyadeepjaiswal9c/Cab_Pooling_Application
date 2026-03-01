# Cab Pooling Application

A desktop application for managing cab pooling services at IIT Patna, built with Python and PyQt5.

## Project Overview
This application facilitates cab pooling among IIT Patna students and faculty, focusing on:
- Campus to Railway Station routes
- Campus to Airport routes
- Festival/Event transportation
- Regular commuter matching

## Features

- **User Management**
  - Secure registration and login
  - Profile management
  - Contact information sharing

- **Trip Management**
  - Create new trips
  - Search available trips
  - Join existing trips
  - Delete created trips
  - View trip details and participants

- **Route Management**
  - Campus-Station routes
  - Campus-Airport routes
  - Event-specific routes
  - Time-based pricing

- **Safety Features**
  - User verification
  - Contact sharing
  - Trip creator information

## Technology Stack

- **Frontend**: PyQt5
- **Backend**: Python 3.x
- **Database**: SQLite
- **Architecture**: MVC Pattern

## Project Structure

```
cab_pooling/
├── main.py                 # Application entry point
├── database/              # Database management
│   ├── db_manager.py      # Database connection and operations
│   └── schema.py          # Database schema definitions
├── controllers/           # Business logic
│   ├── auth.py           # Authentication controller
│   ├── trip.py           # Trip management controller
│   └── search.py         # Search functionality controller
├── models/               # Data models
│   ├── user.py           # User model
│   └── trip.py           # Trip model
└── ui/                   # User interface
    ├── auth_window.py    # Login/Registration window
    ├── main_window.py    # Main application window
    └── trip_dialog.py    # Trip creation dialog
```

## Installation

1. Ensure Python 3.x is installed on your system

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage Guide

1. **Registration**
   - Open the application
   - Click "Sign Up"
   - Enter your details (username, password, email, phone)
   - Click "Create Account"

2. **Creating a Trip**
   - Login to your account
   - Go to "Create Trip" tab
   - Fill in trip details (source, destination, date, time, etc.)
   - Click "Create Trip"

3. **Searching Trips**
   - Go to "Search Trips" tab
   - Enter search criteria
   - View matching trips
   - Click "Join" to join a trip

4. **Managing Your Trips**
   - Go to "My Trips" tab
   - View your created and joined trips
   - Delete trips you've created
   - View trip details and participants

## Future Enhancements

1. **Safety Features**
   - Driver verification
   - Real-time tracking
   - Emergency contacts

2. **Route Optimization**
   - Smart route suggestions
   - Time-based pricing
   - Regular commuter matching

3. **Community Features**
   - User groups
   - Rating system
   - Feedback mechanism

## Contributing

This project was developed as part of the CSE Lab course at IIT Patna.
