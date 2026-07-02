from pathlib import Path

from backend.parsers.candidate_parser import CandidateParser

# Path to dataset
file_path = Path("data/raw/candidates.jsonl")

# Create parser
parser = CandidateParser(file_path)

# Print first 5 candidates
count = 0

for candidate in parser.read_candidates():
    print(candidate)
    count += 1

    if count == 5:
        break