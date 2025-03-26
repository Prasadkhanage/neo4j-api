from neo4j import GraphDatabase
from config import Config

class Neo4jDatabase:
    def __init__(self):
        self.driver = GraphDatabase.driver(Config.NEO4J_URI, auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD))

    def execute_query(self, query: str, params: dict = None):
        try:
            with self.driver.session() as session:
                result = session.run(query, params or {})
                return [record.data() for record in result]
        except Exception as e:
            raise Exception(f"Neo4j Query Error: {str(e)}")

    def close(self):
        self.driver.close()

# Create a global database instance
db = Neo4jDatabase()