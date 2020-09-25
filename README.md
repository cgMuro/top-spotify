## FIND TOP 10 SPOTIFY ARTISTS

This program automates a task that I used to do by hand, wasting a lot of time.
It uses the Spotify API to get the **top 10 artists by monthly listeners** and **top 10 artists by popularity**, then it saves the results in a SQL database (I used MySQL in this project), and then it sends you an email that displays the results in a nice format.

#### Top 10 artists by monthly listeners
The program interacts with the Spotify API to get a playlist that listes the top artists by monthly listeners on Spotify, and then it parses the data to get the top 10 artists.        
This was made possible by this [playlist](https://open.spotify.com/playlist/33Re55lSgkd5XzB6YMhFZA).

#### Top 10 artists by popularity
The program also finds the top 10 artists by popularity, which is a parameter defined inside the Spotify API. This parameter has a value between 0 and 100, and is calculated calculated from the popularity of all the artist’s tracks.


#### Requirements
```
pip install mysql-connector-python
pip install requests
```