from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Evidence:
    doc_type: str
    source: str
    text: str
    score: float

    def to_dict(self):
        return asdict(self)

@dataclass
class SafetyRisk:
    concept: str
    category: str
    rationale: str
    confidence: float
    evidence: List[Evidence]

    def to_dict(self):
        d = asdict(self)
        d['evidence'] = [e.to_dict() for e in self.evidence]
        return d
