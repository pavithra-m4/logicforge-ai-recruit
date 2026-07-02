from pathlib import Path
import os

from flask import (
    Flask,
    render_template,
    request,
    send_file,
    redirect,
    url_for,
    session
)

from docx import Document
from openpyxl import Workbook

from backend.parsers.candidate_parser import CandidateParser
from backend.ranking.ranker import rank_candidates
from backend.ai.reasoning import generate_reason


# -------------------------------------------------
# Flask App
# -------------------------------------------------

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

app.secret_key = "logicforge_secret_key"

UPLOAD_FOLDER = "data/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# -------------------------------------------------
# Home
# -------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------------------------
# Login
# -------------------------------------------------

@app.route("/login")
def login():
    return render_template("login.html")


# -------------------------------------------------
# Dashboard
# -------------------------------------------------

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# -------------------------------------------------
# Upload
# -------------------------------------------------

@app.route("/upload", methods=["POST"])
def upload():

    job = request.files["job_file"]
    candidates = request.files["candidate_file"]

    job_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        job.filename
    )

    candidate_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        candidates.filename
    )

    job.save(job_path)
    candidates.save(candidate_path)

    session["job_path"] = job_path
    session["candidate_path"] = candidate_path

    return redirect(url_for("loading"))


# -------------------------------------------------
# Loading Screen
# -------------------------------------------------

@app.route("/loading")
def loading():
    return render_template("loading.html")


# -------------------------------------------------
# AI Processing
# -------------------------------------------------

@app.route("/process")
def process():

    job_path = session.get("job_path")
    candidate_path = session.get("candidate_path")

    if not job_path or not candidate_path:
        return redirect(url_for("dashboard"))
        # -----------------------------
    # Read Job Description
    # -----------------------------
    job_text = ""

    try:

        if job_path.endswith(".docx"):

            document = Document(job_path)

            for para in document.paragraphs:
                job_text += para.text + " "

        else:

            with open(job_path, "r", encoding="utf-8") as f:
                job_text = f.read()

    except Exception:

        job_text = ""

    # -----------------------------
    # Read Candidates
    # -----------------------------
    parser = CandidateParser(
        Path(candidate_path)
    )

    candidate_list = list(
        parser.read_candidates()
    )

    # -----------------------------
    # Rank Candidates
    # -----------------------------
    ranked = rank_candidates(
        candidate_list
    )

    app.config["RANKED_RESULTS"] = ranked

    top100 = ranked[:100]

    display_candidates = []

    # -----------------------------
    # Build Display Data
    # -----------------------------
    for score, candidate in top100:

        reason = generate_reason(
            candidate,
            score
        )

        profile = candidate.get(
            "profile",
            {}
        )

        display_candidates.append({

            "candidate": candidate,

            "score": round(score, 2),

            "reason": reason,

            "role": profile.get(
                "current_title",
                "Not Available"
            ),

            "company": profile.get(
                "current_company",
                "Not Available"
            ),

            "experience": profile.get(
                "years_of_experience",
                0
            ),

            "summary": profile.get(
                "summary",
                ""
            ),

            "location": profile.get(
                "location",
                ""
            ),

            "education": candidate.get(
                "education",
                []
            ),

            "career": candidate.get(
                "career_history",
                []
            ),

            "skills": candidate.get(
                "skills",
                []
            ),

            "languages": candidate.get(
                "languages",
                []
            )

        })
            # -----------------------------
    # Dashboard Statistics
    # -----------------------------
    total_candidates = len(candidate_list)

    if top100:

        top_score = round(
            top100[0][0],
            2
        )

        excellent = sum(
            1 for score, _ in top100
            if score >= 90
        )

        good = sum(
            1 for score, _ in top100
            if 75 <= score < 90
        )

        average = sum(
            1 for score, _ in top100
            if score < 75
        )

        average_score = round(
            sum(score for score, _ in top100) / len(top100),
            2
        )

    else:

        top_score = 0
        excellent = 0
        good = 0
        average = 0
        average_score = 0

    # -----------------------------
    # Show Results
    # -----------------------------
    return render_template(

        "results.html",

        ranked=display_candidates,

        total_candidates=total_candidates,

        top_score=top_score,

        excellent=excellent,

        good=good,

        average=average,

        average_score=average_score

    )
# -------------------------------------------------
# Download Ranked Output (Excel)
# -------------------------------------------------

@app.route("/download")
def download():

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Ranked Candidates"

    # Header
    sheet.append([
        "Rank",
        "Candidate ID",
        "AI Score"
    ])

    # Candidate Data
    for rank, (score, candidate) in enumerate(
            app.config["RANKED_RESULTS"],
            start=1):

        sheet.append([

            rank,

            candidate["candidate_id"],

            round(score, 2)

        ])

    excel_file = "team_logicforge.xlsx"

    workbook.save(excel_file)

    return send_file(

        excel_file,

        as_attachment=True

    )
# -------------------------------------------------
# Main
# -------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)
