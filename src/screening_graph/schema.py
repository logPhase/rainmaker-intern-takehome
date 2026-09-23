"""What a transaction looks like once it has been read out of a document.

**This is a starting point, not a specification.** Change it, split it, rename it — but keep two
properties, because the grading leans on them:

1. Every field traces back to a document (`doc_ids`).
2. A field the document does not state is `None`, never a guess and never zero.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class DealKind(StrEnum):
    STAKE_PURCHASE = "stake_purchase"
    NEW_SUBSIDIARY = "new_subsidiary"
    MERGER_OR_SCHEME = "merger_or_scheme"
    SLUMP_SALE = "slump_sale"
    DIVESTMENT = "divestment"
    JOINT_VENTURE = "joint_venture"
    OPEN_OFFER = "open_offer"
    ASSET_PURCHASE = "asset_purchase"
    OTHER = "other"


class DealStatus(StrEnum):
    """What the document actually says has happened — not what you infer will happen."""

    BOARD_APPROVED = "board_approved"
    AGREEMENT_SIGNED = "agreement_signed"
    COMPLETED = "completed"
    UNSTATED = "unstated"


class Money(BaseModel):
    """Keep the number and the unit the document used, plus how it was written."""

    amount: float
    currency: str = "INR"
    unit: str = Field(description='as printed: "crore", "lakh", "absolute"')
    as_written: str = Field(description="the exact phrase in the document")


class Party(BaseModel):
    name: str = Field(description="as printed in this document")
    role: str = Field(description='"acquirer" | "target" | "seller"')
    identifier: str | None = Field(default=None, description="CIN, ISIN or exchange symbol, if stated")


class Transaction(BaseModel):
    doc_ids: list[str] = Field(description="every document this rests on")
    kind: DealKind
    status: DealStatus
    parties: list[Party]
    subject_matter: str = Field(description="what was bought: a stake, a business, land, a hospital")
    stake_pct: float | None = None
    consideration: Money | None = None
    announced_on: str | None = Field(default=None, description="ISO date the document is dated")
    completed_on: str | None = None
    evidence: str = Field(description="the sentence(s) you took this from, quoted")
