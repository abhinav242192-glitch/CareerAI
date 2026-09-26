import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "career.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS roadmaps;
DROP TABLE IF EXISTS career_skills;
DROP TABLE IF EXISTS careers;

CREATE TABLE careers (
    career_id INTEGER PRIMARY KEY AUTOINCREMENT,
    career_name TEXT NOT NULL,
    description TEXT NOT NULL,
    demand TEXT NOT NULL
);

CREATE TABLE career_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    career_id INTEGER NOT NULL,
    skill_name TEXT NOT NULL,
    importance TEXT NOT NULL,
    FOREIGN KEY(career_id) REFERENCES careers(career_id)
);

CREATE TABLE roadmaps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    career_id INTEGER NOT NULL,
    step_no INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY(career_id) REFERENCES careers(career_id)
);
""")

careers = [
("AI/ML Engineer","Builds machine learning and AI applications.","High"),
("Data Scientist","Uses data, statistics and machine learning to solve problems.","High"),
("Data Analyst","Analyzes data and creates useful reports and visualizations.","High"),
("Software Developer","Designs, builds and maintains software applications.","High"),
("Web Developer","Builds websites and web applications.","High"),
("Cybersecurity Analyst","Helps protect systems, networks and data.","High"),
("Cloud Engineer","Designs and manages cloud infrastructure and services.","High"),
("DevOps Engineer","Automates software delivery and infrastructure workflows.","High"),
("UI/UX Designer","Designs user interfaces and user experiences.","Medium"),
("Game Developer","Creates interactive games using programming and game technologies.","Medium")
]
cur.executemany("INSERT INTO careers(career_name,description,demand) VALUES(?,?,?)", careers)

career_id = {r[0]: i+1 for i,r in enumerate(careers)}

skills = {
"AI/ML Engineer":[("Python","High"),("Mathematics","High"),("Machine Learning","High"),("Statistics","Medium"),("Data Analysis","Medium")],
"Data Scientist":[("Python","High"),("Statistics","High"),("Data Analysis","High"),("Machine Learning","Medium"),("SQL","Medium")],
"Data Analyst":[("SQL","High"),("Excel","High"),("Data Analysis","High"),("Python","Medium"),("Statistics","Medium")],
"Software Developer":[("Python","Medium"),("C++","Medium"),("Data Structures","High"),("Problem Solving","High"),("Git","Medium")],
"Web Developer":[("HTML/CSS","High"),("JavaScript","High"),("Git","Medium"),("Python","Low"),("Problem Solving","Medium")],
"Cybersecurity Analyst":[("Networking","High"),("Linux","High"),("Python","Medium"),("Cybersecurity","High"),("Problem Solving","Medium")],
"Cloud Engineer":[("Linux","High"),("Networking","High"),("Cloud","High"),("Git","Medium"),("Python","Medium")],
"DevOps Engineer":[("Linux","High"),("Git","High"),("Docker","High"),("Cloud","High"),("Python","Medium")],
"UI/UX Designer":[("UI/UX Design","High"),("Figma","High"),("Communication","Medium"),("Creativity","High")],
"Game Developer":[("C++","High"),("Problem Solving","High"),("Game Development","High"),("Mathematics","Medium")]
}
for name, vals in skills.items():
    cur.executemany("INSERT INTO career_skills(career_id,skill_name,importance) VALUES(?,?,?)",
                    [(career_id[name], s, imp) for s,imp in vals])

roadmaps = {
"AI/ML Engineer":[("Python Fundamentals","Variables, conditions, loops, functions and basic OOP."),
("Python Data Tools","Learn NumPy, Pandas and basic data visualization."),
("Math & Statistics","Cover probability, statistics and linear algebra basics."),
("Machine Learning","Learn regression, classification, clustering and model evaluation."),
("Projects","Build 2–3 small ML projects and document them."),
("Portfolio","Create GitHub projects and prepare for internships.")],
"Data Scientist":[("Python","Learn Python and Pandas."),
("SQL","Learn queries, joins, grouping and databases."),
("Statistics","Learn descriptive statistics and probability."),
("Machine Learning","Study core supervised and unsupervised algorithms."),
("Projects","Build data analysis and ML projects.")],
"Data Analyst":[("Excel","Learn formulas, tables and basic dashboards."),
("SQL","Learn SELECT, JOIN, GROUP BY and subqueries."),
("Python/Pandas","Clean and analyze datasets."),
("Visualization","Create charts and dashboards."),
("Portfolio","Publish practical analysis projects.")],
"Software Developer":[("Programming","Master one programming language."),
("DSA","Learn arrays, strings, stacks, queues, trees and searching."),
("Git","Learn Git and GitHub."),
("Databases","Learn SQL and basic backend concepts."),
("Projects","Build and document applications.")],
"Web Developer":[("HTML/CSS","Build responsive pages."),
("JavaScript","Learn DOM, events and APIs."),
("Git","Track projects with GitHub."),
("Backend Basics","Learn Flask or another backend framework."),
("Projects","Build and deploy web apps.")],
"Cybersecurity Analyst":[("Networking","Learn TCP/IP, DNS, HTTP and common network concepts."),
("Linux","Learn command line and system basics."),
("Security Fundamentals","Study authentication, vulnerabilities and safe testing."),
("Python","Automate simple security-related tasks."),
("Labs","Practice only in legal training environments.")],
"Cloud Engineer":[("Linux","Learn command line and system administration."),
("Networking","Understand IP, DNS, routing and HTTP."),
("Cloud Basics","Learn services from one major cloud platform."),
("Containers","Learn Docker basics."),
("Projects","Deploy a small application.")],
"DevOps Engineer":[("Linux","Learn shell and system basics."),
("Git","Learn branches and collaboration."),
("CI/CD","Understand automated build and test pipelines."),
("Docker","Containerize an application."),
("Cloud","Deploy a small service.")],
"UI/UX Designer":[("Design Principles","Learn layout, hierarchy and accessibility."),
("Figma","Create wireframes and prototypes."),
("User Research","Learn basic user interviews and feedback."),
("Portfolio","Document design decisions and case studies.")],
"Game Developer":[("Programming","Learn C++ or a beginner-friendly game language."),
("Math","Learn vectors, coordinates and basic physics."),
("Game Engine","Learn the basics of a game engine."),
("Projects","Build small playable prototypes.")]
}
for name, steps in roadmaps.items():
    cur.executemany("INSERT INTO roadmaps(career_id,step_no,title,description) VALUES(?,?,?,?)",
                    [(career_id[name], i+1, title, desc) for i,(title,desc) in enumerate(steps)])

conn.commit()
conn.close()
print(f"Database created at {DB_PATH}")
