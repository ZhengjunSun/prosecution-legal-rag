from __future__ import annotations

import re

from .models import LegalResearchReport, Provision, RetrievalHit
from .retrieval import BM25Index


class CitationAgent:
    citation_pattern = re.compile(r"\[(DEMO-\d+)\]")

    def compose(self, question: str, hits: list[RetrievalHit]) -> str:
        if not hits:
            return "演示资料中没有找到足以支持结论的依据，建议转人工核验。"
        evidence = "；".join(
            f"{hit.provision.title}规定：{hit.provision.text}[{hit.provision.provision_id}]"
            for hit in hits
        )
        return f"针对“{question}”，可核验的演示依据如下：{evidence}。最终判断应由专业人员完成。"


class VerificationAgent:
    def verify(self, answer: str, hits: list[RetrievalHit]) -> tuple[str, ...]:
        available = {hit.provision.provision_id for hit in hits}
        cited = set(CitationAgent.citation_pattern.findall(answer))
        findings = [
            f"引用覆盖：{len(cited & available)}/{len(available)}",
            "全部引用均可回链到本次检索结果" if cited <= available else "发现无法回链的引用",
        ]
        for hit in hits:
            findings.append(
                f"{hit.provision.provision_id} 来源={hit.provision.source} "
                f"生效日期={hit.provision.effective_date}"
            )
        return tuple(findings)


class LegalResearchWorkflow:
    def __init__(self, provisions: list[Provision]) -> None:
        self.index = BM25Index(provisions)
        self.writer = CitationAgent()
        self.verifier = VerificationAgent()

    def answer(self, question: str, top_k: int = 3) -> LegalResearchReport:
        hits = self.index.search(question, top_k)
        answer = self.writer.compose(question, hits)
        verification = self.verifier.verify(answer, hits)
        citations = tuple(hit.provision.provision_id for hit in hits)
        return LegalResearchReport(
            question=question,
            answer=answer,
            citations=citations,
            retrieved=tuple(hits),
            verification=verification,
            disclaimer="仅用于技术演示；资料均为虚构，不构成法律意见。",
        )

