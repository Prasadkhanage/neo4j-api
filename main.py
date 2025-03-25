from flask import Flask, request, jsonify
from neo4j import GraphDatabase

# Neo4j Connection Details
NEO4J_URI = "neo4j://<your-neo4j-ip>:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Cd2cNU9UPVOakik"

# Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

app = Flask(__name__)

# Function to Execute Queries
def execute_query(query, params=None):
    try:
        with driver.session() as session:
            result = session.run(query, params or {})
            return [record.data() for record in result]
    except Exception as e:
        return {"error": str(e)}

# API Endpoint to Execute Cypher Queries
@app.route("/execute", methods=["POST"])
def execute_cypher():
    """
    Accepts JSON input:
    {
        "query": "MATCH (n) RETURN n LIMIT 10",
        "params": {}  # Optional parameters
    }
    """
    data = request.json
    query = data.get("query")
    params = data.get("params", {})

    if not query:
        return jsonify({"error": "Query is required"}), 400

    # ❌ Prevent DELETE Queries
    # if "DELETE" in query.upper():
        # return jsonify({"error": "DELETE queries are not allowed"}), 403

    result = execute_query(query, params)
    return jsonify(result)

# Start Flask API Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
