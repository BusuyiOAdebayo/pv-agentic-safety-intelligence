from pathlib import Path
from src.retrieval import DocumentStore
from src.terminology import MedDRALikeMapper
from src.agent import SafetyAgent

ROOT = Path(__file__).parents[1]

def make_agent():
    store = DocumentStore(ROOT/'data/documents')
    mapper = MedDRALikeMapper(ROOT/'data/terminology/meddra_like.csv')
    return SafetyAgent(store, mapper)

def test_meddra_like_mapping():
    agent = make_agent()
    r = agent.answer('MedDRA map: severe headache')
    assert 'PT=Headache' in r['answer']
    assert 'SOC=Nervous system disorders' in r['answer']

def test_liver_answer_is_grounded():
    agent = make_agent()
    r = agent.answer('What is the liver safety profile of AX-101?')
    assert 'ALT' in r['answer'] or 'transaminase' in r['answer']
    assert len(r['citations']) >= 2

def test_anaphylaxis_conflict():
    agent = make_agent()
    r = agent.answer('Is anaphylaxis an identified risk?')
    assert 'not established' in r['answer'].lower()
    assert len(r['citations']) >= 1

def test_profile_generation():
    agent = make_agent()
    r = agent.answer('Generate the compound safety risk profile')
    assert 'nausea' in r['answer'].lower()
    assert 'anaphylaxis' in r['answer'].lower()
