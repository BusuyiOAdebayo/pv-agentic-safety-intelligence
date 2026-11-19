from pathlib import Path
from src.retrieval import DocumentStore
from src.terminology import MedDRALikeMapper
from src.agent import SafetyAgent

ROOT = Path(__file__).parent
agent = SafetyAgent(
    DocumentStore(ROOT / 'data/documents'),
    MedDRALikeMapper(ROOT / 'data/terminology/meddra_like.csv'),
)

QUESTIONS = [
    'What is the liver safety profile of AX-101?',
    'Is anaphylaxis an identified risk?',
    'Generate the compound safety risk profile',
    'MedDRA map: severe headache',
]

for q in QUESTIONS:
    print('\n' + '='*88)
    print('Q:', q)
    result = agent.answer(q)
    print('A:', result['answer'])
    if result['citations']:
        print('Citations:')
        for c in result['citations'][:4]:
            print(f"  - [{c['doc_type']}] {c['source']} (score={c['score']})")
