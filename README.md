# NBA Fantasy Team Manager

This is an app for displaying NBA player performance data 
and displaying statistical calculations about player performance 
and managing fantasy teams in the NBA.

## What it does

- Gets NBA player info from External API
- Inserting data into a PostgreSQL database
- Calculation and presentation of statistical data about the players' performance
- You can make your own fantasy team

## How to use it

1. Make sure you have Python and PostgreSQL

2. Copy the project to your computer:
   ```
   git clone https://github.com/your-username/nba-fantasy-team-manager.git
   cd nba-fantasy-team-manager
   ```

3. Installing the required libraries to run the project:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database (you might need to change some settings):
   ```
   Use the relevant commands in CMD
   Database name: nba_teams
   ```

5. Start the app:
   ```
   flask run in app.py
   ```

6. Go to `http://localhost:5000` in your web browser

## Things you can do

- Look for players: `/api/players/?position={SF}`
- Make a new team: `/api/teams` (you need to send some data)
- See team info: `/api/teams/1` (1 is the team number)
- Change a team: `/api/teams/1` (send new data)
- Delete a team: `/api/teams/1`
- Compare teams: `/api/teams/compare?team1=1&team2=2`

