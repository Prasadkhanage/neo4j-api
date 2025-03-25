import uvicorn
from fastapi import FastAPI, Request, HTTPException
from neo4j import GraphDatabase
from pydantic import BaseModel

# Neo4j Connection Details
NEO4J_URI = "neo4j://4.188.246.244:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Cd2cNU9UPVOakik"

# Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

app = FastAPI()

# Request Model
class QueryRequest(BaseModel):
    query: str
    params: dict = {}

# Function to Execute Queries
def execute_query(query: str, params: dict = None):
    try:
        with driver.session() as session:
            result = session.run(query, params or {})
            return [record.data() for record in result]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API Endpoint to Execute Cypher Queries
@app.post("/execute")
async def execute_cypher(request: QueryRequest):
    """
    Accepts JSON input:
    {
        "query": "MATCH (n) RETURN n LIMIT 10",
        "params": {}  # Optional parameters
    }
    """
    if not request.query:
        raise HTTPException(status_code=400, detail="Query is required")

    # ❌ Prevent DELETE Queries
    # if "DELETE" in request.query.upper():
    #     raise HTTPException(status_code=403, detail="DELETE queries are not allowed")

    return execute_query(request.query, request.params)

# Start FastAPI Server
if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=5000,
        reload=True
    )
