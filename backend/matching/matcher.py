import re


# ============================================================
# IMPORTANT RECRUITMENT TERMS
# ============================================================

TECHNICAL_TERMS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "go",
    "golang",
    "rust",
    "php",
    "ruby",
    "kotlin",
    "swift",

    "sql",
    "mysql",
    "postgresql",
    "postgres",
    "mongodb",
    "redis",
    "oracle",

    "aws",
    "azure",
    "gcp",
    "google cloud",

    "docker",
    "kubernetes",
    "terraform",

    "flask",
    "django",
    "fastapi",
    "spring",
    "react",
    "angular",
    "vue",
    "node",
    "nodejs",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "ai",
    "ml",
    "nlp",
    "computer vision",

    "pytorch",
    "tensorflow",
    "keras",

    "spark",
    "pyspark",
    "hadoop",
    "kafka",
    "airflow",
    "databricks",

    "snowflake",
    "redshift",
    "bigquery",

    "llm",
    "llms",
    "generative ai",
    "genai",
    "rag",
    "langchain",
    "transformers",
    "huggingface",

    "fine tuning",
    "fine-tuning",
    "reinforcement learning",

    "git",
    "github",
    "gitlab",

    "rest",
    "rest api",
    "graphql",

    "linux",
    "bash",

    "tableau",
    "power bi",

    "excel",
    "powerpoint"
}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    if not text:
        return ""

    text = text.lower()

    text = text.replace(
        "fine-tuning",
        "fine tuning"
    )

    text = text.replace(
        "node.js",
        "nodejs"
    )

    text = text.replace(
        "c sharp",
        "c#"
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# EXTRACT RECRUITMENT KEYWORDS
# ============================================================

def extract_keywords(job_text):
    """
    Extract useful technical/recruitment terms from
    the Job Description.

    This deliberately avoids treating every ordinary
    English word as a keyword.
    """

    text = normalize_text(
        job_text
    )

    keywords = set()

    # --------------------------------------------------------
    # First find known multi-word technical terms
    # --------------------------------------------------------

    for term in TECHNICAL_TERMS:

        normalized_term = normalize_text(
            term
        )

        if normalized_term in text:

            keywords.add(
                normalized_term
            )

    # --------------------------------------------------------
    # Extract individual technical words
    # --------------------------------------------------------

    words = re.findall(
        r"[a-zA-Z][a-zA-Z0-9+#.-]*",
        text
    )

    for word in words:

        word = word.lower().strip(
            ".-"
        )

        if word in TECHNICAL_TERMS:

            keywords.add(
                word
            )

    return keywords


# ============================================================
# GET CANDIDATE SKILLS
# ============================================================

def get_candidate_skills(candidate):

    skills = set()

    for skill in candidate.get(
        "skills",
        []
    ):

        if isinstance(
            skill,
            dict
        ):

            name = skill.get(
                "name",
                ""
            )

        else:

            name = str(
                skill
            )

        name = normalize_text(
            name
        )

        if name:

            skills.add(
                name
            )

    return skills


# ============================================================
# FAST MATCH SCORE
# ============================================================

def fast_match_score(
    job_keywords,
    candidate
):
    """
    Extremely lightweight first-stage score.

    Used against large datasets such as 100K candidates.

    It intentionally uses only candidate skills.
    """

    if not job_keywords:

        return 0.0

    candidate_skills = get_candidate_skills(
        candidate
    )

    if not candidate_skills:

        return 0.0

    # --------------------------------------------------------
    # Find matching skills
    # --------------------------------------------------------

    matched = set()

    for job_skill in job_keywords:

        for candidate_skill in candidate_skills:

            if (
                job_skill == candidate_skill
                or
                job_skill in candidate_skill
                or
                candidate_skill in job_skill
            ):

                matched.add(
                    job_skill
                )

                break

    # --------------------------------------------------------
    # Calculate fast percentage
    # --------------------------------------------------------

    score = (
        len(matched)
        /
        len(job_keywords)
    ) * 100

    return round(
        score,
        2
    )


# ============================================================
# DETAILED MATCHING
# ============================================================

def calculate_match(
    job_text,
    candidate
):
    """
    Detailed matching used after the fast
    pre-screening stage.
    """

    job_keywords = extract_keywords(
        job_text
    )

    candidate_skills = get_candidate_skills(
        candidate
    )

    if not job_keywords:

        return (
            0,
            [],
            list(candidate_skills)
        )

    matched = set()
    missing = set()

    # --------------------------------------------------------
    # Compare JD skills with candidate skills
    # --------------------------------------------------------

    for job_skill in job_keywords:

        found = False

        for candidate_skill in candidate_skills:

            if (
                job_skill == candidate_skill
                or
                job_skill in candidate_skill
                or
                candidate_skill in job_skill
            ):

                matched.add(
                    job_skill
                )

                found = True

                break

        if not found:

            missing.add(
                job_skill
            )

    # --------------------------------------------------------
    # JD match percentage
    # --------------------------------------------------------

    match_percent = (
        len(matched)
        /
        len(job_keywords)
    ) * 100

    match_percent = round(
        match_percent,
        2
    )

    return (
        match_percent,
        sorted(matched),
        sorted(missing)
    )