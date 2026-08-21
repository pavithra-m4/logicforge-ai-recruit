import json
from pathlib import Path


class CandidateParser:
    """
    Streams candidates from a JSONL dataset.

    Candidates are yielded one at a time instead of
    loading the complete dataset into memory.
    """

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def read_candidates(self):

        valid_count = 0
        invalid_count = 0

        with self.file_path.open(
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            for line_number, line in enumerate(
                file,
                start=1
            ):

                line = line.strip()

                if not line:
                    continue

                try:

                    candidate = json.loads(line)

                    if isinstance(
                        candidate,
                        dict
                    ):

                        valid_count += 1

                        yield candidate

                    else:

                        invalid_count += 1

                except json.JSONDecodeError:

                    invalid_count += 1

                    continue

        print(
            f"Candidate parsing complete: "
            f"{valid_count} valid, "
            f"{invalid_count} invalid records skipped."
        )