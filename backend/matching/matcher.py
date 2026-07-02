import re


def extract_keywords(job_text):
    """
    Extract keywords from Job Description.
    """

    words = re.findall(r"[A-Za-z0-9+#.]+", job_text.lower())

    stop_words = {
        "the", "and", "or", "with", "for", "to", "of",
        "in", "on", "at", "a", "an", "is", "are",
        "will", "be", "as", "by", "from"
    }

    keywords = set()

    for word in words:

        if len(word) > 2 and word not in stop_words:
            keywords.add(word)

    return keywords


def calculate_match(job_text, candidate):

    jd_keywords = extract_keywords(job_text)

    candidate_skills = {
        skill["name"].lower()
        for skill in candidate.get("skills", [])
    }

    matched = jd_keywords.intersection(candidate_skills)

    missing = candidate_skills - matched

    if len(candidate_skills) == 0:
        return 0, [], []

    match_percent = min(
    100,
    round((len(matched) / len(candidate_skills)) * 130, 2)
)

    return (
        match_percent,
        list(matched),
        list(missing)
    )