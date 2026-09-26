from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from pathlib import Path
from models.recommendation_model import recommend_careers, skill_gap, roadmap_for

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "career.db"

app = Flask(__name__)
app.secret_key = "careerai-demo-secret-key"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/assessment")
def assessment():
    conn = get_db()
    careers = conn.execute("SELECT * FROM careers ORDER BY career_name").fetchall()
    skills = conn.execute("SELECT DISTINCT skill_name FROM career_skills ORDER BY skill_name").fetchall()
    conn.close()
    return render_template("assessment.html", careers=careers, skills=skills)

@app.route("/submit", methods=["POST"])
def submit():
    profile = {
        "name": request.form.get("name", "Student").strip() or "Student",
        "branch": request.form.get("branch", "B.Tech CSE").strip(),
        "semester": request.form.get("semester", "1"),
        "interest": request.form.get("interest", "").strip(),
        "subject": request.form.get("subject", "").strip(),
        "experience": request.form.get("experience", "None"),
        "skills": request.form.getlist("skills"),
        "career_preference": request.form.get("career_preference", "").strip()
    }
    results = recommend_careers(profile)
    session["profile"] = profile
    session["results"] = results
    return redirect(url_for("results"))

@app.route("/results")
def results():
    profile = session.get("profile")
    results = session.get("results")
    if not profile or not results:
        return redirect(url_for("assessment"))
    top = results[0]
    gaps = skill_gap(profile, top["career_id"])
    roadmap = roadmap_for(top["career_id"])
    return render_template("results.html", profile=profile, results=results, top=top, gaps=gaps, roadmap=roadmap)

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").lower().strip()
    replies = [
        (["ai", "machine learning", "ml"], "For AI/ML, start with Python, NumPy, Pandas, basic statistics, then machine learning and small projects."),
        (["data analyst", "data analysis"], "A Data Analyst roadmap can start with Excel, SQL, Python/Pandas, statistics, visualization and portfolio projects."),
        (["software", "developer", "coding"], "For software development, build programming fundamentals, DSA, Git/GitHub, databases and projects."),
        (["cyber", "security", "cybersecurity"], "For cybersecurity, learn networking, Linux, Python, security fundamentals and safe lab-based practice."),
        (["cloud", "devops"], "For cloud/DevOps, learn Linux, networking, Git, Docker basics and one cloud platform."),
        (["start", "beginner", "coding nahi", "don't know coding"], "If you are a beginner, start with Python basics for 30–45 minutes daily, then build a very small project."),
        (["resume", "cv"], "Build a simple one-page resume with education, skills, projects, achievements and links to your portfolio/GitHub."),
    ]
    for keywords, reply in replies:
        if any(k in message for k in keywords):
            return jsonify({"reply": reply})
    return jsonify({"reply": "Tell me the career you are interested in, your current skills, or what you want to learn. I can suggest a starting roadmap."})

if __name__ == "__main__":
    app.run(debug=True)
