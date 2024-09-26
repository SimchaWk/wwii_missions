# WWII Missions Database Project

This is an application for managing and displaying data about World War II aerial bombing missions. It provides
statistical calculations and management of mission-related information.

## What it does

- Stores and manages data about WWII aerial bombing missions
- Inserts and retrieves data from a PostgreSQL database
- Provides statistical calculations about mission performance
- Allows management of countries, cities, targets, and mission details

## How to use it

1. Make sure you have Python and PostgreSQL installed

2. Copy the project to your computer:
   ```
   git clone https://github.com/SimchaWk/wwii_missions.git
   ccd wwii-missions
   ```

3. Installing the required libraries to run the project:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database (Not required, can be created by running the software):
   ```
   Use the relevant commands in CMD
   Database name: wwii_missions
   ```

5. Start the app:
   ```
   flask run in app.py
   ```

6. Go to `http://localhost:5000` in your web browser

## Things you can do

- Get all missions: `GET /missions`
- Get a specific mission: `GET /missions/<id>`
- Create a new country: `POST /countries` (you need to send some data)
- Get country info: `GET /countries/<id>`
- Update a country: `PUT /countries/<id>` (send new data)
- Delete a country: `DELETE /countries/<id>`
- Get cities by country: `GET /cities?country_id=<id>`
- Create a new target: `POST /targets` (you need to send some data)
- Get targets by priority: `GET /targets?priority=<priority>`
- Update a target: `PUT /targets/<id>` (send new data)
- Delete a target: `DELETE /targets/<id>`

## Additional Information

- The project uses Flask for the web framework
- SQLAlchemy is used for database operations
- The `returns` library is used for functional programming concepts
- Error handling and input validation are implemented throughout the application