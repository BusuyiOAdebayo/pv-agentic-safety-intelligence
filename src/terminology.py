import csv
from difflib import SequenceMatcher

class MedDRALikeMapper:
    """License-safe demo mapper using a tiny synthetic MedDRA-like hierarchy.

    This is NOT the MedDRA dictionary and must not be used for clinical coding.
    """
    def __init__(self, csv_path: str):
        with open(csv_path, newline='', encoding='utf-8') as f:
            self.rows = list(csv.DictReader(f))

    def map_term(self, term: str):
        term_l = term.lower().strip()
        best, best_score = None, -1.0
        for row in self.rows:
            candidates = [row['reported_term'], row['llt'], row['pt']]
            score = max(SequenceMatcher(None, term_l, c.lower()).ratio() for c in candidates)
            if term_l in [c.lower() for c in candidates]:
                score = 1.0
            if score > best_score:
                best, best_score = row, score
        return {**best, 'match_score': round(best_score, 3)} if best else None
