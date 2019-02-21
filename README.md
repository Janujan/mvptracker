# NBA MVP Tracker
This is a django app to track the NBA MVP race for the 2018-2019 season. This application uses BasketballReference data to analyze the top players in the league and provide a recent history of their performances through the season.

The application uses a PostGreSQL database to store player data and is deployed on Heroku.

A link to the application can be found [here](https://intense-hamlet-29591.herokuapp.com/mvp/)

### Blog
I've also created a blogging feature to allow for any extended analysis that I would like to highlight from my own experimentation with the data.


## Approach
I wanted to follow object oriented design when designing the system around players. I wanted to capture real time data that can update player stats as the season progressed. With these two design goals in mind, I proceeded to build a Django app that uses the MTV architecture to store and display player data. Once the app was fully functioning, I created a background process to be run daily on Heroku to update the states stored in the database. This can be considered as a nightly patch to capture new performances for each player.


## Implementation
The key models I used to design the database system were `Player` and `Game`. Each `Player` model corresponds with a player in the NBA and stores their current season totals for all counting stats. Each `Player` has a Many-To-One relationship with a  `Game` model. A `Game` model stores the date of the game as well as the player's stat totals for the game.


## Next Steps
The next major step I want to take is to improve my ranking algorithm to better capture guard performance as rebounds seem to overpower all other counting stats.
I also want to improve efficiency of the database by having a single `Game` entry capturing all player performances for that game so that there can be a Many-To-Many relationship between `Players` and `Games`.
