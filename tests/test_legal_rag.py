from legal_rag.cli import demo_provisions
from legal_rag.retrieval import BM25Index
from legal_rag.workflow import LegalResearchWorkflow


def test_retrieval_prefers_procedural_record() -> None:
    hits = BM25Index(demo_provisions()).search("自动化建议保留检索依据和人工复核记录")
    assert hits[0].provision.provision_id == "DEMO-102"


def test_every_citation_is_verified() -> None:
    report = LegalResearchWorkflow(demo_provisions()).answer("证据来源如何审查？")
    retrieved_ids = {hit.provision.provision_id for hit in report.retrieved}
    assert set(report.citations) == retrieved_ids
    assert "无法回链" not in " ".join(report.verification)
    assert report.disclaimer


def test_no_evidence_means_no_confident_answer() -> None:
    report = LegalResearchWorkflow(demo_provisions()).answer("quantum banana spacecraft")
    assert not report.citations
    assert "没有找到" in report.answer

