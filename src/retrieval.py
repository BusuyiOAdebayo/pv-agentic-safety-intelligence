from pathlib import Path
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Evidence

class DocumentStore:
    def __init__(self, docs_dir: str):
        self.docs = []
        for path in sorted(Path(docs_dir).glob('*.md')):
            text = path.read_text(encoding='utf-8')
            doc_type = self._extract_doc_type(text, path.stem)
            for i, chunk in enumerate(self._chunk(text)):
                self.docs.append({
                    'doc_type': doc_type,
                    'source': f'{path.name}#chunk-{i+1}',
                    'text': chunk,
                })
        corpus = [d['text'] for d in self.docs]
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
        self.matrix = self.vectorizer.fit_transform(corpus)

    @staticmethod
    def _extract_doc_type(text, fallback):
        m = re.search(r'Document type:\s*([^\n]+)', text, flags=re.I)
        return m.group(1).strip() if m else fallback.upper()

    @staticmethod
    def _chunk(text, max_chars=650):
        paras = [p.strip() for p in text.split('\n\n') if p.strip()]
        chunks, cur = [], ''
        for p in paras:
            if cur and len(cur)+len(p)+2 > max_chars:
                chunks.append(cur)
                cur = p
            else:
                cur = f'{cur}\n\n{p}'.strip()
        if cur:
            chunks.append(cur)
        return chunks

    def search(self, query: str, k: int = 5):
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix)[0]
        idx = scores.argsort()[::-1][:k]
        return [Evidence(self.docs[i]['doc_type'], self.docs[i]['source'], self.docs[i]['text'], float(scores[i])) for i in idx if scores[i] > 0]
