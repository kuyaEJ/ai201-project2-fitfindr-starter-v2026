import re
import math

# ==========================================
# 1. TEXT SEARCH ENGINE (BM25 + FIELD WEIGHTS)
# ==========================================
def tokenize(text: str) -> list[str]:
    """Helper: Extracts lowercase alphanumeric words."""
    if not text:
        return []
    return re.findall(r'\b[a-z0-9]+\b', str(text).lower())

class BM25SearchEngine:
    def __init__(self, listings: list[dict], k1=1.5, b=0.75):
        self.listings = listings
        self.k1 = k1
        self.b = b
        self.doc_tokens = []
        
        # Build weighted document representations:
        # Title repeated 5x (5x weight), Tags 3x (3x weight), Description 1x
        for item in listings:
            title_part = (item.get('title', '') + " ") * 5
            tags_part = (" ".join(item.get('style_tags', [])) + " ") * 3
            desc_part = item.get('description', '')
            colors_part = item.get('colors', [])
            combined = f"{title_part} {tags_part} {desc_part} {colors_part}"
            self.doc_tokens.append(tokenize(combined))
            
        self.doc_lens = [len(doc) for doc in self.doc_tokens]
        self.avgdl = sum(self.doc_lens) / len(self.doc_lens) if self.doc_lens else 1.0
        self.idf = self._compute_idf()

    def _compute_idf(self) -> dict[str, float]:
        N = len(self.listings)
        doc_freq = {}
        for doc in self.doc_tokens:
            for word in set(doc):
                doc_freq[word] = doc_freq.get(word, 0) + 1
        
        idf = {}
        for word, freq in doc_freq.items():
            idf[word] = math.log((N - freq + 0.5) / (freq + 0.5) + 1.0)
        return idf

    def get_text_scores(self, query: str) -> list[float]:
        query_tokens = tokenize(query)
        scores = []
        
        for idx, doc in enumerate(self.doc_tokens):
            score = 0.0
            doc_len = self.doc_lens[idx]
            word_counts = {}
            for word in doc:
                word_counts[word] = word_counts.get(word, 0) + 1
                
            for q_token in query_tokens:
                if q_token not in word_counts:
                    continue
                f = word_counts[q_token]
                idf_val = self.idf.get(q_token, 0.0)
                
                num = f * (self.k1 + 1)
                den = f + self.k1 * (1 - self.b + self.b * (doc_len / self.avgdl))
                score += idf_val * (num / den)
                
            scores.append(score)
        return scores