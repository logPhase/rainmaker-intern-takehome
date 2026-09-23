"""Loading transactions into Graphiti, and querying them back. Yours to write.

Read the Graphiti docs first: https://help.getzep.com/graphiti — especially how an episode is
added, what `group_id` scopes, and which timestamp Graphiti treats as "when this was true".

`docker compose up -d` gives you FalkorDB on localhost:6379.
"""

from __future__ import annotations

from .schema import Transaction


async def build_graph(transactions: list[Transaction]) -> None:
    """Load these transactions into the graph."""
    raise NotImplementedError


async def search(query: str) -> list[dict]:
    """Search the graph. Shape the return value to whatever `ask.py` needs."""
    raise NotImplementedError
