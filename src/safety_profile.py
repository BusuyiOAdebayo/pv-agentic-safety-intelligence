from .models import SafetyRisk

CONCEPTS = {
    'nausea': ['nausea'],
    'headache': ['headache'],
    'pyrexia': ['pyrexia', 'fever'],
    'rash': ['rash'],
    'hepatic enzyme elevation': ['alt elevation', 'alt elevations', 'transaminase', 'hepatic enzyme', 'liver-enzyme'],
    'anaphylaxis': ['anaphylaxis', 'hypersensitivity'],
}

class SafetyProfiler:
    def __init__(self, store):
        self.store = store

    def _evidence_for(self, concept):
        q = concept + ' adverse reaction risk safety'
        return self.store.search(q, k=8)

    def build(self):
        risks = []
        for concept, terms in CONCEPTS.items():
            ev = self._evidence_for(concept)
            joined = ' '.join(e.text.lower() for e in ev)
            if not any(t in joined for t in terms):
                continue
            if any(x in joined for x in ['identified risks:', 'established adverse reactions', 'very common:', 'most common adverse reactions']):
                category, conf = 'identified risk / established adverse reaction', 0.90
            elif any(x in joined for x in ['potential risk:', 'causality remains uncertain', 'possibly related', 'ongoing surveillance']):
                category, conf = 'potential risk / signal under evaluation', 0.72
            else:
                category, conf = 'observed event / monitor', 0.60
            if concept == 'hepatic enzyme elevation':
                category, conf = 'potential risk / monitored laboratory abnormality', 0.82
            if concept == 'anaphylaxis':
                category, conf = 'potential risk / signal under evaluation', 0.70
            rationale = self._rationale(concept, ev, category)
            risks.append(SafetyRisk(concept, category, rationale, conf, ev[:4]))
        return risks

    @staticmethod
    def _rationale(concept, evidence, category):
        docs = sorted(set(e.doc_type for e in evidence))
        return f'{concept.title()} is classified as {category} based on converging or unresolved evidence across {", ".join(docs)}.'
