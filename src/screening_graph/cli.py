"""The `screening-graph` command line.

`corpus` works out of the box, so you can check your environment before writing anything. The
other three commands are yours. Keep them, add to them, or restructure them — but one command
per stage, and `--help` should tell a stranger how to run the pipeline.
"""

from __future__ import annotations

import typer

from . import corpus
from .ask import QUESTION_IDS

app = typer.Typer(add_completion=False, help="Build a screening graph from Indian exchange filings.")


@app.command("corpus")
def corpus_cmd(kind: str = typer.Option(None, help="filing | news")) -> None:
    """List the shipped documents. Use this to check your setup."""
    docs = corpus.documents(kind)
    for doc in docs:
        label = doc.subject or doc.title or ""
        typer.echo(f"{doc.doc_id}  {doc.kind:7}  {(doc.company_name or '')[:34]:34}  {label[:44]}")
    typer.echo(f"\n{len(docs)} documents")


@app.command()
def extract(
    doc_id: str = typer.Option(None, help="one document; default is all of them"),
    out: str = typer.Option("out/transactions.json", help="where to write the result"),
) -> None:
    """Read transactions out of the documents."""
    raise NotImplementedError("implement extract: see src/screening_graph/extract.py")


@app.command()
def load(src: str = typer.Option("out/transactions.json")) -> None:
    """Load extracted transactions into Graphiti."""
    raise NotImplementedError("implement load: see src/screening_graph/graph.py")


@app.command()
def ask(
    question: str = typer.Argument(None, help=f"one of {', '.join(QUESTION_IDS)}"),
    all_questions: bool = typer.Option(False, "--all", help="answer every question in QUESTIONS.md"),
) -> None:
    """Answer the questions in QUESTIONS.md from the graph."""
    raise NotImplementedError("implement ask: see src/screening_graph/ask.py")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
