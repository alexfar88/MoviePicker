🎬🎬🎬 MoviePicker 🎬🎬🎬

MoviePicker is a Python tool that helps you pick a random movie to watch from your list.  
It fetches movie info from the OMDb API, lets you filter by genre, and allows you to mark movies as watched.  

## Important Notes ##
- You can use your **own movie list** please just make sure it is saved as a `.txt` file (**with one movie per line**).  
- The program will automatically create and update a `movies.csv` file, so you don’t need to make this yourself.  
- Marking movies as "Watched" will update `movies.csv` so they won’t be suggested again.  

## Features ##
- Can suggests a random unwatched movie based off selected genres 
- Mark movies as watched manually or after viewing a suggestion  
- Stores your collection in a CSV file  

## Usage ##
1. Add your movie titles to `movies.txt` (one per line).  
2. Run `movies_data.py` to fetch details from OMDb and save to `movies.csv`.  
3. Run `suggest_movie.py` to get a movie recommendation or update watched status.
