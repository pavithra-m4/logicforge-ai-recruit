import json
from pathlib import Path

from backend.models.candidate import Candidate


class CandidateParser:
    """
    Reads candidates from the JSONL dataset.
    """

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def read_candidates(self):
        with self.file_path.open("r", encoding="utf-8") as file:
            for line in file:
                data = json.loads(line)
                yield data