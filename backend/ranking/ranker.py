from backend.ranking.scoring import calculate_score


def rank_candidates(candidates):

    ranked = []

    # Calculate raw scores
    for candidate in candidates:

        raw_score = calculate_score(candidate)

        ranked.append((raw_score, candidate))

    # Sort by raw score
    ranked.sort(reverse=True, key=lambda x: x[0])

    # Normalize to 0-100
    if ranked:

        max_score = ranked[0][0]

        normalized = []

        for score, candidate in ranked:

            final_score = round((score / max_score) * 100, 2)

            normalized.append((final_score, candidate))

        return normalized

    return []