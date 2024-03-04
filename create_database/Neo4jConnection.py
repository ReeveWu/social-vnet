from neo4j import GraphDatabase

class Neo4jConnection:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def create_movie_graph(self, movie_title, overview, genres, directing):
        with self.__driver.session() as session:
            result = session.write_transaction(self._create_and_return_movie, movie_title, overview, genres, directing)
            print("Created movie graph for:", result)
    
    @staticmethod
    def _create_and_return_movie(tx, movie_title, overview, genres, directing):
        overview = overview if overview else "No overview provided"
        genres = genres if genres else []
        directing = directing if directing else []
        
        query = (
            "MERGE (m:Movie {title: $movie_title, overview: $overview}) "
            "FOREACH (genre in $genres | "
            "   MERGE (g:Genre {name: genre}) "
            "   MERGE (m)-[:HAS_GENRE]->(g)) "
            "FOREACH (director in $directing | "
            "   MERGE (d:Director {name: director}) "
            "   MERGE (m)-[:HAS_DIRECTOR]->(d)) "
            "RETURN m.title AS title"
        )
        result = tx.run(query, movie_title=movie_title, overview=overview, genres=genres, directing=directing)
        return result.single()[0]
    
    def delete_all(self):
        with self.__driver.session() as session:
            session.write_transaction(self._delete_all_nodes_and_relations)
            print("Deleted all nodes and relations.")

    @staticmethod
    def _delete_all_nodes_and_relations(tx):
        query = "MATCH (n) DETACH DELETE n"
        tx.run(query)