from pathlib import Path
import streamlit as st
from src.retrieval import DocumentStore
from src.terminology import MedDRALikeMapper
from src.agent import SafetyAgent

ROOT = Path(__file__).parent
store = DocumentStore(ROOT/'data/documents')
mapper = MedDRALikeMapper(ROOT/'data/terminology/meddra_like.csv')
agent = SafetyAgent(store, mapper)

st.set_page_config(page_title='PV Agentic Safety Intelligence', layout='wide')
st.title('PV Agentic Safety Intelligence')
st.caption('Synthetic, license-safe demo: RAG + agentic reasoning + MedDRA-like normalization + compound safety profiling')

question = st.text_input('Ask a safety/regulatory question', 'What is the liver safety profile of AX-101?')
if st.button('Analyze'):
    result = agent.answer(question)
    st.subheader('Evidence-backed answer')
    st.write(result['answer'])
    st.subheader('Source-level citations')
    for c in result['citations']:
        st.markdown(f"**{c['doc_type']} — {c['source']}** (retrieval score {c['score']})")
        st.caption(c['excerpt'])

with st.expander('Try these questions'):
    st.code('What is the liver safety profile of AX-101?\nIs anaphylaxis an identified risk?\nGenerate the compound safety risk profile\nMedDRA map: severe headache')
