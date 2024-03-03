import os
import requests
from dotenv import load_dotenv

load_dotenv()

tmdb_authorization = os.getenv('TMDB_API_KEY')

def get_movie_id(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?query={movie_title}&include_adult=false&language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": tmdb_authorization
    }

    response = requests.get(url, headers=headers)
    movie_id = response.json()['results'][0]['id']

    return movie_id


def get_tmdb_data(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?append_to_response=credits&language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": tmdb_authorization
    }

    response = requests.get(url, headers=headers)
    response = response.json()

    data = {
        "movie_id": movie_id,
        "title": response['title'],
        "overview": response['overview'],
        "genres": [genre['name'] for genre in response['genres']],
        "stars": response['vote_average'],
        "acting": list(set([actor['name'] for actor in response['credits']['cast']])), 
        "writing": list(set([crew['name'] for crew in response['credits']['crew'] if crew['known_for_department'] == "Writing"])),
        "directing": list(set([crew['name'] for crew in response['credits']['crew'] if crew['known_for_department'] == "Directing"])),
    }

    return data
