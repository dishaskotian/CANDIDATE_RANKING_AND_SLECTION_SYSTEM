from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# ------------------ DB Connection ------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",         # replace with your MySQL username
    password="Disha@124",     # replace with your MySQL password
    database="candidate_db"
)
cursor = db.cursor(dictionary=True)


# ------------------ Routes ------------------

@app.route("/")
def home():
    return render_template("index.html")


# Add Candidate
@app.route("/add_candidate", methods=["POST"])
def add_candidate():
    data = request.json
    sql = """INSERT INTO candidates
             (First_Name, Last_Name, Contact_Info, Degree, Grad_Year, Education, Experience, Application_Date)
             VALUES (%s,%s,%s,%s,%s,%s,%s,CURDATE())"""
    vals = (
        data["First_Name"], data["Last_Name"], data["Contact_Info"],
        data.get("Degree", ""), data["Grad_Year"], data.get("Education", ""),
        data["Experience"]
    )
    cursor.execute(sql, vals)
    candidate_id = cursor.lastrowid  

    # Insert into candidate_skills table
    if "Skill" in data and data["Skill"]:
        cursor.execute("SELECT Skill_ID FROM skill WHERE Skill_Name=%s", (data["Skill"],))
        skill = cursor.fetchone()
        if skill:
            cursor.execute("INSERT INTO candidate_skills (Candidate_ID, Skill_ID) VALUES (%s, %s)",
                           (candidate_id, skill["Skill_ID"]))

    db.commit()
    return jsonify({"message": "Candidate added successfully"})



# Update Candidate
@app.route("/update_candidate", methods=["POST"])
def update_candidate():
    data = request.json
    sql = """UPDATE candidates 
             SET First_Name=%s, Last_Name=%s, Contact_Info=%s, Degree=%s, Grad_Year=%s, Education=%s, Experience=%s
             WHERE Candidate_ID=%s"""
    vals = (
        data["First_Name"], data["Last_Name"], data["Contact_Info"],
        data.get("Degree", ""), data["Grad_Year"], data.get("Education", ""),
        data["Experience"], data["Candidate_ID"]
    )
    cursor.execute(sql, vals)
    db.commit()
    return jsonify({"message": "Candidate updated successfully"})


# Evaluate Candidate (with Evaluation Type)
@app.route("/evaluate_candidate", methods=["POST"])
def evaluate_candidate():
    data = request.json
    sql = """INSERT INTO evaluation (Candidate_ID, Score, Feedback, Evaluation_Type, Evaluation_Date)
             VALUES (%s,%s,%s,%s,CURDATE())"""
    vals = (
        data["Candidate_ID"],
        data["Score"],
        data.get("Feedback", ""),
        data.get("Evaluation_Type", "General")
    )
    cursor.execute(sql, vals)
    db.commit()
    return jsonify({"message": "Evaluation submitted"})


# Show All Candidates
@app.route("/all_candidates", methods=["GET"])
def all_candidates():
    cursor.execute("SELECT * FROM candidates")
    result = cursor.fetchall()
    return jsonify(result)


# Top Candidate
@app.route("/top_candidate", methods=["GET"])
def top_candidate():
    cursor.execute("""SELECT c.Candidate_ID, c.First_Name, c.Last_Name, AVG(e.Score) as Final_Score
                      FROM candidates c
                      JOIN evaluation e ON c.Candidate_ID = e.Candidate_ID
                      GROUP BY c.Candidate_ID
                      ORDER BY Final_Score DESC
                      LIMIT 1""")
    result = cursor.fetchone()
    return jsonify(result)



# ------------------ Run ------------------
if __name__ == "__main__":
    app.run(debug=True)
