from pathlib import Path

from backend.parsers.candidate_parser import CandidateParser
from backend.ranking.ranker import rank_candidates

parser = CandidateParser(Path("data/raw/candidates.jsonl"))

candidates = []

count = 0

for c in parser.read_candidates():
    candidates.append(c)

    count += 1

    if count == 100:
        break

ranked = rank_candidates(candidates)

for score, candidate in ranked[:10]:
    print(score, candidate["candidate_id"])