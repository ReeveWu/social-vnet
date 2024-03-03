import time
import pandas as pd
from utils import get_movie_info

df = pd.read_csv('../data/vodclickstream_uk_movies_03.csv')
movie_df = pd.read_csv('../data/movie_data.csv')

movie_titles = list(set(df['title'].values) - set(movie_df['netflix_title'].values))
print(f"Total:", len(movie_titles))

error_count = 0

for i, movie_title in enumerate(movie_titles):
    try:
        movie_id = get_movie_info.get_movie_id(movie_title)
        movie_info = get_movie_info.get_tmdb_data(movie_id)
        movie_info['netflix_title'] = movie_title
        movie_df = pd.concat([movie_df, pd.DataFrame([movie_info])], ignore_index=True)
        movie_df.to_csv('../data/movie_data.csv', index=False)
        time.sleep(0.05)
    except:
        error_count += 1
        print(f"Error ID: {i}, Name: {movie_title}, Count: {error_count}")

print("Done!")
while True:
    time.sleep(1)