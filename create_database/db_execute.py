import os
import time
import pandas as pd
from dotenv import load_dotenv
from Neo4jConnection import Neo4jConnection

load_dotenv()

uri = os.getenv('NEO4J_CONNECTION_URL')
user = os.getenv('NEO4J_USER')
password = os.getenv('NEO4J_PASSWORD')
print(uri)

def insert(conn: Neo4jConnection, movie_title: str, overview: str, genres: list, acting: list, directing: list):
    overview = "" if pd.isna(overview) else overview
    genres = [] if pd.isna(genres) else eval(genres)
    acting = [] if pd.isna(acting) else eval(acting)
    directing = [] if pd.isna(directing) else eval(directing)

    conn.create_movie_graph(movie_title, overview, genres, acting, directing)

def truncate(conn):
    conn.delete_all()

if __name__ == "__main__":
    conn = Neo4jConnection(uri, user, password)

    truncate(conn)

    df = pd.read_csv('../data/movie_data_filtered.csv')
    data = df.to_dict(orient='records')
    print("Total:", len(data))
    for d in data:
        try:
            insert(conn=conn, 
                movie_title=d['title'].strip(), 
                overview=d['overview'].strip(), 
                genres=d['genres'], 
                acting=d['acting'], 
                directing=d['directing']
                )
        except Exception as e:
            print(f"Error: {e}")
            
    conn.close()

    print("Done!")

    while True:
        time.sleep(1)