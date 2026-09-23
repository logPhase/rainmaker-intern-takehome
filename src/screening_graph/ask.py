"""Answering the questions in QUESTIONS.md from the graph. Yours to write.

Each answer carries the `doc_id`s it rests on and a line saying how it was derived.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Answer:
    question_id: str  # "Q1" .. "Q6"
    answer: str
    doc_ids: list[str] = field(default_factory=list)
    derivation: str = ""


QUESTION_IDS = ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6")


async def answer(question_id: str) -> Answer:
    raise NotImplementedError
