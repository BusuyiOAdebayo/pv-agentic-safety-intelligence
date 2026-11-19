# PV Agentic Safety Intelligence

A compact, interview-ready pharmacovigilance and regulatory-intelligence demo that extends an agentic scientific platform into drug-safety reasoning.

## What it demonstrates

- **RAG over safety/regulatory documents** with source-level citations.
- **Agentic routing** between document search, safety profiling, and terminology normalization.
- **MedDRA-like adverse-event normalization** using a tiny synthetic hierarchy: LLT -> PT -> HLT -> HLGT -> SOC.
- **Cross-document reconciliation** across synthetic CTD, RMP, SmPC, USPI, DSUR, and PBRER-style evidence.
- **Compound-level safety profiling** into identified risks, potential risks/signals, and monitored abnormalities.
- **Grounding and hallucination mitigation** by restricting answers to retrieved evidence and surfacing citations.
- **Deterministic regression tests** for terminology mapping, liver-safety reasoning, anaphylaxis conflict handling, and profile generation.

> **Important:** This repository is a technical demonstration only. It does not provide medical advice, does not perform validated pharmacovigilance, and must not be used for clinical or regulatory decisions.

## Why the terminology is synthetic

MedDRA is a licensed terminology. To keep this public repository license-safe, `data/terminology/meddra_like.csv` contains only a small synthetic hierarchy that mirrors the official five-level structure for demonstration purposes. It is **not MedDRA** and is not suitable for clinical coding.

The official MedDRA hierarchy is: **System Organ Class (SOC) -> High Level Group Term (HLGT) -> High Level Term (HLT) -> Preferred Term (PT) -> Lowest Level Term (LLT)**.

## Architecture

```text
User question
    |
    v
SafetyAgent (router)
    |----------------------|----------------------|
    v                      v                      v
Document RAG          Safety Profiler       MedDRA-like Mapper
    |                      |                      |
TF-IDF vector search   Cross-document        LLT->PT->HLT->
+ metadata/citations   risk synthesis        HLGT->SOC
    |                      |                      |
    -----------------------|----------------------
                           v
                Evidence-backed answer
                + source-level citations
```

## Demo corpus

All documents are synthetic and describe fictional compound **AX-101**:

- CTD clinical safety summary
- Risk Management Plan (RMP)
- Summary of Product Characteristics (SmPC)
- US Prescribing Information (USPI)
- Development Safety Update Report (DSUR)
- Periodic Benefit-Risk Evaluation Report (PBRER)

The corpus intentionally includes both consistent and conflicting evidence:

- nausea/headache: established/common adverse reactions
- hepatic enzyme elevations: reversible, monitored, potential risk
- anaphylaxis: reported but causality unresolved

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Example questions

```text
What is the liver safety profile of AX-101?
Is anaphylaxis an identified risk?
Generate the compound safety risk profile
MedDRA map: severe headache
```

## Run tests

```bash
pytest -q
```

## Project structure

```text
pv-agentic-safety-intelligence/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── documents/
│   │   ├── ctd_safety_summary.md
│   │   ├── dsur.md
│   │   ├── pbrer.md
│   │   ├── rmp.md
│   │   ├── smpc.md
│   │   └── uspi.md
│   └── terminology/
│       └── meddra_like.csv
├── src/
│   ├── agent.py
│   ├── models.py
│   ├── retrieval.py
│   ├── safety_profile.py
│   └── terminology.py
└── tests/
    └── test_app.py
```

## How this maps to real pharmacovigilance work

This demo is intentionally small, but the production extension path is straightforward:

1. Replace TF-IDF with sentence embeddings + **pgvector/Qdrant/Milvus**.
2. Replace synthetic terminology with a properly licensed MedDRA integration.
3. Add document parsers for real eCTD/RMP/SmPC/USPI/DSUR/PBRER source files.
4. Add structured extraction for adverse events, seriousness, expectedness, causality, frequency, and exposure.
5. Add signal-detection statistics and case-level aggregation.
6. Add LLM generation through Bedrock/Claude/OpenAI with citation enforcement.
7. Add human-in-the-loop medical review, audit trail, model/version logging, and validated controls.

## Regulatory context used for the design

The design follows public regulatory concepts rather than reproducing proprietary content:

- EMA describes RMPs as containing a medicine's safety profile, risk-minimisation measures, and plans to further characterize safety.
- EMA places the RMP in CTD section 1.8.2 and requires version control for submissions.
- SmPC is a routine EU risk-minimisation tool.
- MedDRA uses a five-level hierarchy from LLT through SOC.

## Interview talking points

- **MedDRA:** “I implemented a license-safe MedDRA-like normalizer to demonstrate LLT-to-PT-to-SOC coding logic; production use would require a licensed dictionary.”
- **Cross-document reasoning:** “The agent reconciles evidence across RMP, CTD, SmPC, USPI, DSUR, and PBRER-style documents rather than answering from one source.”
- **Safety-risk generation:** “The compound profiler distinguishes established risks from potential signals and monitored abnormalities and links each classification back to evidence.”
- **Hallucination mitigation:** “Answers are constrained to retrieved evidence, citations are surfaced, and unsupported risk claims are intentionally avoided.”
- **Research-to-production:** “The demo includes UI, retrieval layer, agent logic, terminology mapping, safety-profile generation, tests, and a clear production migration path.”

## Disclaimer

Fictional compound, synthetic documents, synthetic terminology, and heuristic classifications. Not a validated medical, regulatory, or pharmacovigilance system.
