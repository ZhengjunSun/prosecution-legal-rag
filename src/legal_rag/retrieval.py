from __future__ import annotations

import math
import re
from collections import Counter

from .models import Provision, RetrievalHit

TOKEN = re.compile(r"[\u4e00-\u9fff]|[A-Za-z0-9]+")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN.findall(text)]


class BM25Index:
    def __init__(self, provisions: list[Provision], k1: float = 1.5, b: float = 0.75) -> None:
        if not provisions:
            raise ValueError("provisions must not be empty")
        self.provisions = provisions
        self.k1 = k1
        self.b = b
        self.docs = [tokenize(f"{p.title} {p.text}") for p in provisions]
        self.avg_len = sum(map(len, self.docs)) / len(self.docs)
        self.document_frequency: Counter[str] = Counter()
        for doc in self.docs:
            self.document_frequency.update(set(doc))

    def search(self, query: str, top_k: int = 3) -> list[RetrievalHit]:
        query_terms = tokenize(query)
        hits: list[RetrievalHit] = []
        for provision, doc in zip(self.provisions, self.docs):
            frequencies = Counter(doc)
            score = 0.0
            for term in query_terms:
                df = self.document_frequency[term]
                if not df:
                    continue
                inverse_frequency = math.log(1 + (len(self.docs) - df + 0.5) / (df + 0.5))
                tf = frequencies[term]
                denominator = tf + self.k1 * (1 - self.b + self.b * len(doc) / self.avg_len)
                score += inverse_frequency * tf * (self.k1 + 1) / denominator
            if score > 0:
                hits.append(RetrievalHit(provision, round(score, 4)))
        return sorted(hits, key=lambda hit: hit.score, reverse=True)[:top_k]

