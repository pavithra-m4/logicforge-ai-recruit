def calculate_score(candidate):
    """
    Calculate a candidate profile quality score from 0-100.

    This score is NOT the Job Description match.
    It represents the overall strength of the candidate profile.

    Used as 30% of the final recruitment score.
    """

    profile = candidate.get(
        "profile",
        {}
    )

    signals = candidate.get(
        "redrob_signals",
        {}
    )

    skills = candidate.get(
        "skills",
        []
    )

    score = 0.0

    # ========================================================
    # 1. EXPERIENCE — 25 POINTS
    # ========================================================

    experience = profile.get(
        "years_of_experience",
        0
    )

    try:
        experience = float(
            experience
        )
    except (
        ValueError,
        TypeError
    ):
        experience = 0

    # 10+ years receives full points.
    experience_score = min(
        experience / 10,
        1
    ) * 25

    score += experience_score

    # ========================================================
    # 2. PROFILE COMPLETENESS — 15 POINTS
    # ========================================================

    completeness = signals.get(
        "profile_completeness_score",
        0
    )

    try:
        completeness = float(
            completeness
        )
    except (
        ValueError,
        TypeError
    ):
        completeness = 0

    # Dataset completeness is already 0-100.
    completeness_score = (
        min(
            max(
                completeness,
                0
            ),
            100
        ) / 100
    ) * 15

    score += completeness_score

    # ========================================================
    # 3. OPEN TO WORK — 10 POINTS
    # ========================================================

    if signals.get(
        "open_to_work_flag",
        False
    ):

        score += 10

    # ========================================================
    # 4. RECRUITER RESPONSE RATE — 15 POINTS
    # ========================================================

    response_rate = signals.get(
        "recruiter_response_rate",
        0
    )

    try:
        response_rate = float(
            response_rate
        )
    except (
        ValueError,
        TypeError
    ):
        response_rate = 0

    response_rate = min(
        max(
            response_rate,
            0
        ),
        1
    )

    score += response_rate * 15

    # ========================================================
    # 5. TECHNICAL SKILL DEPTH — 20 POINTS
    # ========================================================

    if skills:

        skill_scores = []

        for skill in skills:

            if not isinstance(
                skill,
                dict
            ):
                continue

            proficiency = str(
                skill.get(
                    "proficiency",
                    ""
                )
            ).lower()

            if proficiency == "advanced":

                skill_scores.append(
                    1.0
                )

            elif proficiency == "intermediate":

                skill_scores.append(
                    0.7
                )

            elif proficiency == "beginner":

                skill_scores.append(
                    0.4
                )

            else:

                skill_scores.append(
                    0.5
                )

        if skill_scores:

            average_skill_strength = (
                sum(skill_scores)
                /
                len(skill_scores)
            )

            # More useful skills also contribute,
            # but cap the contribution.

            skill_count_factor = min(
                len(skill_scores) / 10,
                1
            )

            technical_score = (
                average_skill_strength
                *
                skill_count_factor
                *
                20
            )

            score += technical_score

        # ========================================================
    # 6. GITHUB / TECHNICAL ACTIVITY — 10 POINTS
    # ========================================================

    github_activity = signals.get(
        "github_activity_score",
        0
    )

    try:
        github_activity = float(
            github_activity
        )
    except (
        ValueError,
        TypeError
    ):
        github_activity = 0

    github_activity = min(
        max(
            github_activity,
            0
        ),
        10
    )

    score += (
        github_activity / 10
    ) * 10

    # ========================================================
    # 7. CAREER / PROFILE EVIDENCE — 5 POINTS
    # ========================================================

    career_history = candidate.get(
        "career_history",
        []
    )

    education = candidate.get(
        "education",
        []
    )

    certifications = candidate.get(
        "certifications",
        []
    )

    evidence_score = 0

    if career_history:
        evidence_score += 3

    if education:
        evidence_score += 1

    if certifications:
        evidence_score += 1

    score += evidence_score

    # ========================================================
    # FINAL NORMALIZATION
    # ========================================================

    return round(
        min(
            max(
                score,
                0
            ),
            100
        ),
        2
    )
    # ========================================================
    # FINAL NORMALIZATION
    # ========================================================

    return round(
        min(
            max(
                score,
                0
            ),
            100
        ),
        2
    )