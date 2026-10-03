from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Provision:
    provision_id: str
    title: str
    text: str
    effective_date: str
    source: str


@dataclass(frozen=True)
class RetrievalHit:
    provision: Provision
    score: float


@dataclass(frozen=True)
class LegalResearchReport:
    question: str
    answer: str
    citations: tuple[str, ...]
    retrieved: tuple[RetrievalHit, ...]
    verification: tuple[str, ...]
    disclaimer: str

    def to_dict(self) -> dict:
        return asdict(self)

