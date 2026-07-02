def generate_reason(candidate, score):

    profile = candidate.get("profile", {})

    role = profile.get("current_title", "Professional")

    experience = profile.get("years_of_experience", 0)

    skills = candidate.get("skills", [])

    top_skills = []

    for skill in skills[:5]:
        top_skills.append(skill.get("name", ""))

    skill_text = ", ".join(top_skills)

    if score >= 90:
        status = "Excellent match"

    elif score >= 75:
        status = "Good match"

    elif score >= 60:
        status = "Average match"

    else:
        status = "Low match"

    return (
        f"{status} • "
        f"{role} • "
        f"{experience} yrs experience • "
        f"Skills: {skill_text}"
    )