# FastAPI Movie Booking System

## Overview

This is a fully functional example project built with Python and FastAPI, designed as an **Online Ticket Booking System**. The project demonstrates fundamental FastAPI concepts while simulating a simple cinema hall management system. Instead of using a database, this project stores data in JSON format.

### Features
- Role-based authentication system (Admin and Member users)
- Secure login with bcrypt hashing
- Admin can add movies for a specific day and time
- Members can reserve and unreserve seats until all are booked

## Installation Guide

Follow these steps to set up the project:

1. **Clone the repository**
   ```sh
   git clone https://github.com/SujishMaharjan/movie_booking-fastapi.git
   ```
2. **Navigate to the project directory**
   ```sh
   cd movie_booking-fastapi
   ```
3. **Create and activate a virtual environment**
   ```sh
   python -m venv env
   
   # Activate the environment
   # On Windows
   env\Scripts\activate
   
   # On macOS/Linux
   source env/bin/activate
   ```
4. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
5. **Run the application**
   ```sh
   fastapi dev server.py
   ```

## Usage

- Access the API documentation at `http://127.0.0.1:8000/docs`
- Use the interactive Swagger UI to test API endpoints



## Contributing
Feel free to fork this repository and submit pull requests with improvements or new features.

