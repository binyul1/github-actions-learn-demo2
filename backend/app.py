import mysql.connector
import os
from flask import Flask, jsonify, request
 
app = Flask(__name__)
 
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )
 
def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users")
    result = cursor.fetchall()
    conn.close()
    return [r[0] for r in result]
 
@app.route("/")
def home():
    return """
<h1>Welcome to Flask App created by binyul</h1>
<p>Use the following curl commands to interact with the API:</p>
<ul>
<li><b>View users:</b><br>
<code>curl http://localhost:5000/api/users</code></li>
<li><b>Add a user:</b><br>
<code>curl -X POST http://localhost:5000/api/users -H "Content-Type: application/json" -d '{"name":"NewStudent"}'</code></li>
</ul>
    """
 
@app.route("/api/users", methods=["GET"])
def users():
    return jsonify(get_users())
 
@app.route("/api/users", methods=["POST"])
def add_user():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400
 
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"User {name} added successfully!"}), 201

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)