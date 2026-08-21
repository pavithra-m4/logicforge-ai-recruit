from backend.ranking.scoring import calculate_score
from backend.matching.matcher import calculate_match


def rank_candidates(
    candidates,
    job_text=""
):
    """
    Rank candidates using a genuine 0-100 score.

    The score is based on:
        - Job Description match
        - Experience
        - Candidate profile signals
        - Technical skills
    """

    ranked = []

    for candidate in candidates:

        # --------------------------------------------------
        # Job-specific match
        # --------------------------------------------------

        if job_text:

            job_match, matched, missing = calculate_match(
                job_text,
                candidate
            )

        else:

            job_match = 0
            matched = []
            missing = []

        # --------------------------------------------------
        # Existing candidate profile score
        # --------------------------------------------------

        profile_score = calculate_score(
            candidate
        )

        # calculate_score should represent
        # candidate quality from 0-100.
        profile_score = min(
            max(
                profile_score,
                0
            ),
            100
        )

        # --------------------------------------------------
        # Final score
        # --------------------------------------------------
        #
        # Job match       = 70%
        # Candidate profile = 30%
        #
        # Job-specific fit is intentionally dominant.
        # --------------------------------------------------

        final_score = (
            job_match * 0.70
            +
            profile_score * 0.30
        )

        final_score = round(
            min(
                max(
                    final_score,
                    0
                ),
                100
            ),
            2
        )

        # Store matching information
        # so the results page can display it.

        candidate["_job_match_score"] = round(
            job_match,
            2
        )

        candidate["_profile_score"] = round(
            profile_score,
            2
        )

        candidate["_matched_skills"] = matched

        candidate["_missing_skills"] = missing

        ranked.append(
            (
                final_score,
                candidate
            )
        )

    # ------------------------------------------------------
    # Highest score first
    # ------------------------------------------------------

    ranked.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return ranked