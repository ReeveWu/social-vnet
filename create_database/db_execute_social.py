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

def insert(conn: Neo4jConnection, user_id: str, movie_title: str):
    conn.create_social_graph(user_id, movie_title)

def truncate(conn):
    conn.delete_all()

if __name__ == "__main__":
    conn = Neo4jConnection(uri, user, password)

    df = pd.read_csv('../data/movie_data_filtered.csv')
    movie_title_dict = df.set_index('netflix_title')['title'].to_dict()

    df = pd.read_csv('../data/user_record_filtered.csv')
    data = df.to_dict(orient='records')
    print("Total:", len(data))
    for i, d in enumerate(data):
        print(f"Round: {i}/{len(data)}")
        if movie_title_dict.get(d['title'], None) is None:
            continue
        try:
            insert(conn=conn, 
                user_id=d['user_id'].strip(),
                movie_title=movie_title_dict[d['title']].strip(), 
                )
        except Exception as e:
            print(f"Error: {e}")
            
    conn.close()

    print("Done!")

    while True:
        time.sleep(1)