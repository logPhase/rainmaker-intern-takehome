"""Document text -> `Transaction` objects. Yours to write.

Two things worth deciding before you start:

- how you tell a transaction document from one that merely mentions companies, and
- what you do when a field is only half-stated (a stake with no consideration, a consideration
  with no closing date).
"""

from __future__ import annotations

from .corpus import Document
from .schema import Transaction


async def extract(document: Document) -> list[Transaction]:
    """Return the transactions this document describes. Empty list if it describes none."""
    raise NotImplementedError
