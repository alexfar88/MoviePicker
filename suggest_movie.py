import pandas as pd
import questionary

####################
CSVfile = "movies.csv"
df = pd.read_csv(CSVfile)

#Ask to suggest or mark a movie as watched
action = questionary.select("What would you like to do?",
                            choices= ["Suggest a movie to watch","Mark a movie as watched", "Cancel"]
).ask()

if action == "Mark a movie as watched":
    movie_to_mark = questionary.autocomplete("Type the movie you would like to mark as watched: ",
                                             choices = df["Title"].tolist()).ask()
    if movie_to_mark: # updates the watched column
        df.loc[df["Title"]== movie_to_mark,"Watched"] = "Yes"
        df.to_csv(CSVfile, index=False)
        print(f"{movie_to_mark} marked as watched!")
    else:
        print("No movie selected")

elif action == "Suggest a movie to watch":
    ##########
    #gather all the genres
    all_genres = []
    for g in df["Genre"].dropna():
        for genre in g.split(","):
           genre = genre.strip()
           if genre not in all_genres:
               all_genres.append(genre)

    all_genres.sort()

    #select prompt
    selected_genres = questionary.checkbox(
        "Select one or more genres(blank to skip):", choices=all_genres).ask()

####  filter out watched movies ###
    unwatched = df[df["Watched"] == "No"]

    #used to narrow down movies selected by genre
    def genre_match(genres,selected): 
        return any(g in genres for g in selected)

    if selected_genres: # gets both lower case for matching
        selected_genres = [g.lower() for g in selected_genres]
         #filters unwatched down to match selected genres
        unwatched = unwatched[unwatched["Genre"].str.lower().str.split(", ")
                              .apply(genre_match, selected=selected_genres)]


    #### pick a movie now ###
    if unwatched.empty:
        print("No movies left for the selected genres")
    else: 
        movie = unwatched.sample(1).iloc[0]
        print(f"Tonight's movie is: {movie['Title']} from {movie['Year']}")


    ### mark movie as watched? ###
    response = questionary.select("Did you watch this movie?",
                                   choices=["Yes, I did","No, maybe later"]).ask()

    if response == "Yes, I did":
        df.loc[df["Title"]== movie["Title"],"Watched"] = "Yes"
        df.to_csv(CSVfile, index=False)
        print(f"{movie['Title']} marked as watched!")
    else:
        print("Movie will be saved for later recommendation")
    ########
else:
    print("Bye!")
