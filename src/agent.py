from .safety_profile import SafetyProfiler

class SafetyAgent:
    def __init__(self, store, mapper):
        self.store = store
        self.mapper = mapper
        self.profiler = SafetyProfiler(store)

    def answer(self, question: str):
        q = question.lower()
        if 'meddra' in q or 'map' in q:
            term = question.split(':',1)[1].strip() if ':' in question else question
            mapped = self.mapper.map_term(term)
            if not mapped:
                return self._package('No terminology match found.', [])
            ans = (f"Demo terminology mapping: '{term}' -> LLT={mapped['llt']} -> PT={mapped['pt']} -> "
                   f"HLT={mapped['hlt']} -> HLGT={mapped['hlgt']} -> SOC={mapped['soc']} "
                   f"(match={mapped['match_score']}).")
            return self._package(ans, [])

        if any(x in q for x in ['anaphylaxis', 'liver', 'hepatic', 'alt', 'transaminase']):
            evidence = self.store.search(question, k=6)
            answer = self._synthesize(question, evidence)
            return self._package(answer, evidence)

        if 'profile' in q or 'risk' in q:
            profile = self.profiler.build()
            lines = ['Compound safety profile for AX-101:']
            citations = []
            for r in profile:
                lines.append(f'- {r.concept}: {r.category} (confidence {r.confidence:.2f}). {r.rationale}')
                citations.extend(r.evidence[:2])
            return self._package('\n'.join(lines), citations)

        evidence = self.store.search(question, k=6)
        answer = self._synthesize(question, evidence)
        return self._package(answer, evidence)

    @staticmethod
    def _synthesize(question, evidence):
        if not evidence:
            return 'I could not find supporting evidence in the demo corpus.'
        q = question.lower()
        if 'anaphylaxis' in q:
            return ('Anaphylaxis is not established as an identified risk in the demo corpus. A DSUR case was possibly related but confounded, '
                    'and the PBRER states causality remains uncertain with ongoing surveillance warranted.')
        if 'liver' in q or 'hepatic' in q or 'alt' in q:
            return ('Reversible ALT/transaminase elevations are consistently described across the CTD, RMP, SmPC, USPI and DSUR-style documents. '
                    'The evidence supports monitoring and a potential-risk classification, but the demo corpus does not establish severe drug-induced liver injury.')
        return ('Evidence was retrieved from the demo safety/regulatory corpus. The highest-ranking passages are cited below; '
                'the system intentionally avoids claims not supported by those passages.')

    @staticmethod
    def _package(answer, evidence):
        seen, cites = set(), []
        for e in evidence:
            if e.source not in seen:
                seen.add(e.source)
                cites.append({'source': e.source, 'doc_type': e.doc_type, 'score': round(e.score,3), 'excerpt': e.text[:280]})
        return {'answer': answer, 'citations': cites}
