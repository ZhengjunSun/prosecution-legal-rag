from __future__ import annotations

import argparse
import json

from .models import Provision
from .workflow import LegalResearchWorkflow


def demo_provisions() -> list[Provision]:
    return [
        Provision(
            "DEMO-101",
            "演示规范：证据审查",
            "审查材料时，应核对来源、形成过程以及不同材料之间能否相互印证。",
            "2026-01-01",
            "fictional://demo-code",
        ),
        Provision(
            "DEMO-102",
            "演示规范：程序记录",
            "自动化系统生成的建议应保留检索依据、处理步骤和人工复核记录。",
            "2026-01-01",
            "fictional://demo-code",
        ),
        Provision(
            "DEMO-103",
            "演示规范：个人信息",
            "处理个人信息时，应遵循目的明确、范围最小和访问留痕的原则。",
            "2026-01-01",
            "fictional://demo-code",
        ),
        Provision(
            "DEMO-104",
            "演示规范：不确定性",
            "依据不足或者存在冲突时，系统不得给出确定性结论，应提示人工核验。",
            "2026-01-01",
            "fictional://demo-code",
        ),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the fictional legal RAG demo")
    parser.add_argument("question", nargs="?", default="自动化建议为什么需要保留依据和人工复核？")
    args = parser.parse_args()
    report = LegalResearchWorkflow(demo_provisions()).answer(args.question)
    print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

