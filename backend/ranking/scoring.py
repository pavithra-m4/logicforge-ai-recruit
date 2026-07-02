def calculate_score(candidate):

    score = 0

    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})

    # Experience
    exp = profile.get("years_of_experience", 0)

    if 5 <= exp <= 9:
        score += 20

    # Open to Work
    if signals.get("open_to_work_flag"):
        score += 15

    # Recruiter Response Rate
    score += signals.get("recruiter_response_rate", 0) * 20

    # Profile Completeness
    score += signals.get("profile_completeness_score", 0) / 5

    # GitHub Activity
    github = signals.get("github_activity_score", -1)

    if github > 0:
        score += github

    return score