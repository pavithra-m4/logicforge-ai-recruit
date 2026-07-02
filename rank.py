import json
import csv
from pathlib import Path

CANDIDATES_FILE = Path("data/raw/candidates.jsonl")
OUTPUT_FILE = "submission.csv"


AI_KEYWORDS = {
    "python",
    "llm",
    "nlp",
    "retrieval",
    "ranking",
    "embedding",
    "embeddings",
    "vector",
    "pinecone",
    "weaviate",
    "qdrant",
    "milvus",
    "faiss",
    "elasticsearch",
    "opensearch",
    "rag",
    "transformer",
    "bert",
    "sentence-transformers",
    "fine-tuning",
    "lora",
    "qlora",
    "pytorch",
    "tensorflow",
    "machine learning",
    "deep learning",
    "airflow",
    "spark",
    "pyspark"
}

PRODUCT_COMPANIES = {
    "Google",
    "Microsoft",
    "Amazon",
    "Meta",
    "OpenAI",
    "Flipkart",
    "Swiggy",
    "Zomato",
    "Razorpay",
    "PhonePe",
    "Freshworks",
    "Zoho"
}


def calculate_score(candidate):

    score = 0.0

    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})

    # -------------------------
    # Experience
    # -------------------------
    exp = profile.get("years_of_experience", 0)

    if 5 <= exp <= 9:
        score += 15
    elif exp >= 3:
        score += 8

    # -------------------------
    # Skills
    # -------------------------
    skills = candidate.get("skills", [])

    skill_names = {
        s.get("name", "").lower()
        for s in skills
    }

    for kw in AI_KEYWORDS:
        if kw.lower() in skill_names:
            score += 3

    # -------------------------
    # Career History
    # -------------------------
    history = candidate.get("career_history", [])

    for job in history:

        desc = job.get("description", "").lower()

        if "retrieval" in desc:
            score += 6

        if "ranking" in desc:
            score += 6

        if "recommendation" in desc:
            score += 6

        if "embedding" in desc:
            score += 6

        if "vector" in desc:
            score += 6

        company = job.get("company", "")

        if company in PRODUCT_COMPANIES:
            score += 4

    # -------------------------
    # Redrob Signals
    # -------------------------

    if signals.get("open_to_work_flag"):
        score += 5

    score += signals.get("profile_completeness_score", 0) / 20

    score += signals.get("recruiter_response_rate", 0) * 10

    github = signals.get("github_activity_score", -1)

    if github > 0:
        score += github

    if signals.get("notice_period_days", 999) <= 30:
        score += 4

    if signals.get("willing_to_relocate"):
        score += 2

    return round(score, 4)


def build_reason(candidate):

    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})

    return (
        f"{profile.get('years_of_experience',0)} yrs experience, "
        f"{profile.get('current_title','')} at "
        f"{profile.get('current_company','')}; "
        f"OpenToWork={signals.get('open_to_work_flag',False)}, "
        f"RecruiterResponse={signals.get('recruiter_response_rate',0):.2f}"
    )


def main():

    ranked = []

    with open(CANDIDATES_FILE, "r", encoding="utf-8") as f:

        for line in f:

            candidate = json.loads(line)

            score = calculate_score(candidate)

            ranked.append((score, candidate))

    ranked.sort(
        key=lambda x: (
            -x[0],
            x[1]["candidate_id"]
        )
    )

    top100 = ranked[:100]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow(
            [
                "candidate_id",
                "rank",
                "score",
                "reasoning",
            ]
        )

        for rank, (score, candidate) in enumerate(top100, start=1):

            writer.writerow(
                [
                    candidate["candidate_id"],
                    rank,
                    score,
                    build_reason(candidate),
                ]
            )

    print("submission.csv generated successfully")


if __name__ == "__main__":
    main()