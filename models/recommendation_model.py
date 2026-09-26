from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "career.db"

def get_career_data():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    careers = conn.execute("SELECT * FROM careers").fetchall()
    skill_rows = conn.execute("SELECT * FROM career_skills").fetchall()
    conn.close()

    skills = {}
    for row in skill_rows:
        skills.setdefault(row["career_id"], []).append(dict(row))
    return [dict(c) for c in careers], skills

def recommend_careers(profile):
    careers, skills = get_career_data()
    interest = profile["interest"].lower()
    subject = profile["subject"].lower()
    experience = profile["experience"].lower()
    selected = {s.lower() for s in profile.get("skills", [])}
    preference = profile.get("career_preference", "").lower()

    results = []
    for career in careers:
        career_text = f'{career["career_name"]} {career["description"]}'.lower()
        score = 0.0
        reasons = []

        if interest and interest in career_text:
            score += 25
            reasons.append("your selected interest matches this career")
        if subject and subject in career_text:
            score += 15
            reasons.append("your preferred subject is relevant")
        if preference and preference in career["career_name"].lower():
            score += 20
            reasons.append("it matches your stated career preference")
        if experience != "none":
            score += 5

        required = skills.get(career["career_id"], [])
        if required:
            matched = 0
            for item in required:
                if item["skill_name"].lower() in selected:
                    matched += 1
            score += (matched / len(required)) * 35

        score = min(98.0, round(score, 1))
        if not reasons:
            reasons.append("your profile has some transferable skills or interests")
        results.append({
            "career_id": career["career_id"],
            "career_name": career["career_name"],
            "description": career["description"],
            "demand": career["demand"],
            "score": score,
            "reason": "; ".join(reasons)
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:5]

def skill_gap(profile, career_id):
    _, skills = get_career_data()
    selected = {s.lower() for s in profile.get("skills", [])}
    gap = []
    for item in skills.get(career_id, []):
        if item["skill_name"].lower() not in selected:
            gap.append({"skill": item["skill_name"], "importance": item["importance"]})
    return gap

def roadmap_for(career_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT step_no, title, description FROM roadmaps WHERE career_id=? ORDER BY step_no",
        (career_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
