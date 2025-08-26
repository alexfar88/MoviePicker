import requests
import pandas as pd
import os
import sys
import questionary

#### constants for API Key and file names ####
API_KEY = "c0599d48"  # OMDb API key
INPUT_FILE = "movies.txt"
OUTPUT_FILE = "movies.csv"

def fetch_movie_data(title):
####
# Fetches movie data from OMDb API by title, then 
# returns a dictionary with relevant fields, else returns None
####
    url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get("Response") == "True":
        return {
            "Title": data["Title"],
            "Year": data["Year"],
            "Genre": data["Genre"],
            "Watched": "No"  # default
        }
    else:
        print(f"Could not find movie named: {title}")
        return None

# add a new movie to the list #
def add_movie(title, output=OUTPUT_FILE):
    new_data = fetch_movie_data(title)
    if not new_data:
        return # if no data was found it stops and doesn't make a new csv
    #checks to see if the movies.csv file already exists
    if os.path.exists(OUTPUT_FILE): 
        existing_df = pd.read_csv(OUTPUT_FILE)

        #prevents duplicate movies
        if title.lower() in existing_df["Title"].str.lower().values:
            print(f"{title} is already in the list")
            return 
        # adds the new movie
        new_df = pd.DataFrame([new_data])
        updated = pd.concat([existing_df, new_df], ignore_index=True)

        updated.to_csv(OUTPUT_FILE,index = False, encoding = "utf-8")
    else:
        #if the file isn't made this creates it
        pd.DataFrame([new_data]).to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    
    print(f"{title} successfully added to the list")
        
def create_new_csv(input_file=INPUT_FILE, output_file=OUTPUT_FILE):
    # Read movie titles line by line
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        titles = [line.strip() for line in f if line.strip()]
    # get data on the movies
    movies_data = []
    for title in titles:
        if title:
            data = fetch_movie_data(title)
            movies_data.append(data)
    # make the df with no none
    cleaned_data = []
    for m in movies_data:
        if m is not None:
            cleaned_data.append(m)
    #now creates dataframe and saves as csv
    df = pd.DataFrame(cleaned_data)

    # turn it into a csv
    df.to_csv(OUTPUT_FILE,index=False,encoding="utf-8")


    print(f"A movie list has been made, named {OUTPUT_FILE}")


########################
#___ Ask what to do ___#
########################
action = questionary.select(
    "What would you like to do?",
    choices=[
        "Create a NEW movie list",
        "Add a movie to the existing list",
        "Exiting"
    ]
).ask()

if action == "Create a NEW movie list":
    create_new_csv()
elif action == "Add a movie to the existing list":
    #first check to see if a movie csv list exists
    if not os.path.exists(OUTPUT_FILE):
        print(f"{OUTPUT_FILE} does not exist, please first create a movie list")
    else:   
        movie_name = questionary.text("Enter the movie title:").ask()
        add_movie(movie_name)
else:
    print("Exiting")


