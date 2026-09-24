# Take-home: build a screening graph from Indian exchange filings

**Time budget: one weekend, 8–12 hours.** If you spend much longer, stop and tell us what you cut —
knowing what to leave out is part of the job.

## The business problem

We build software for M&A advisers. Before an adviser approaches a buyer, they need to know what
that buyer has actually been doing: what it bought, from whom, for how much, and when. That
evidence sits in public filings — companies tell the exchanges every time they buy a stake, form a
subsidiary, merge, or sell a business — and in the press, which reports the same deals in different
words and sometimes with different numbers.

Today an analyst reads those filings by hand. Your job is a small version of the machine that reads
them instead.

**A word on why this is hard.** An adviser will put your output in front of a client. A number you
invent, or a deal you attribute to the wrong company, is worse than an empty field. Empty is honest;
wrong is a lost client. Design for that.

## What you get

Everything is in `data/`, already fetched for you. No scraping needed.

| | Count | What it is |
|---|---|---|
| `data/filings/FIL-*.txt` | 34 | Real announcements filed with the NSE in Aug–Sep 2026, as text pulled from the filed PDF |
| `data/pdf/FIL-*.pdf` | 34 | The original PDFs, if you prefer to parse them yourself |
| `data/news/NEWS-*.json` | 12 | Google News headlines about some of the same companies (headline, publisher, date, link — no article body) |
| `data/manifest.json` | — | One row per document: `doc_id`, company, subject, date, source URL, file paths |

Some filings describe a transaction. **Some describe nothing of the sort** — a record date, an
investor call, a board appointment. Both kinds are in there on purpose.

## What to build

A small pipeline, driven by a CLI, that does four things:

1. **Extract.** For each document, pull out the transaction it describes: who acquired what from
   whom, the stake, the consideration, the date, and the kind of deal (stake purchase, new
   subsidiary, merger or scheme, slump sale, divestment, joint venture, open offer, land or asset
   purchase). Documents with no transaction must produce nothing.
2. **Load.** Put the results into a temporal knowledge graph using **Graphiti**
   (<https://github.com/getzep/graphiti>), with a backing graph database (a `docker-compose.yml` for
   FalkorDB is included). Model the entities and relationships yourself.
3. **Ask.** Answer the six questions in `QUESTIONS.md` from the graph — not from a hardcoded table,
   and not by re-reading the files at question time. **Every answer must cite the `doc_id`s it rests
   on.**
4. **Tell us what you found.** A short `NOTES.md`: what you'd do differently with another week,
   where your extraction is weakest, what Graphiti did well and badly, and what the run cost.

Hand in a library plus that CLI, with tests. No UI.

## Rules

- **Graphiti is required.** You probably have not used it. That is the point: we want to see how you
  pick up something unfamiliar. Its docs are good; read them before you write code.
- **Every stored value must come from a document.** If the filing does not state the consideration,
  the field is empty. Never estimate, never fill a gap with a plausible number, never let the model
  "reason" a figure into existence.
- **Distinguish what was stated from what you concluded.** A filing that says "the Board approved the
  acquisition" has not said the deal completed. Your schema should be able to tell those apart.
- **No hand-written answers.** If we change a document, your answers should change.
- **Keep secrets out of git.** Use `.env` (see `.env.example`); it is already in `.gitignore`.
- **Use of AI coding tools is fine and expected.** You will be asked about any line of it.

## Getting started

```bash
uv sync                      # Python 3.11+, uv: https://docs.astral.sh/uv/
cp .env.example .env         # put the API key we sent you in here
docker compose up -d         # FalkorDB for Graphiti
uv run screening-graph --help
uv run pytest
```

Before your first run, read [Your API key and the setup traps](#your-api-key-and-the-setup-traps)
below. It will save you an evening.

## Your API key and the setup traps

These are about getting the environment to run, not about the exercise. Everyone hits them, so
here they are up front.

**The key is an OpenRouter key, not an OpenAI key.** OpenRouter speaks the OpenAI API at
`https://openrouter.ai/api/v1`. Model names carry the provider: `openai/gpt-4.1-mini`,
`openai/text-embedding-3-small`.

**It has a hard $10 spending cap and expires 7 days after we send it.** After either, requests
fail. A full run over the corpus costs well under $1, but a runaway loop will empty it in minutes:
put a limit on retries before you add them. If a bug burns the key, tell us; we will top it up.

**Graphiti reaches for OpenAI in three places.** The LLM, the embedder *and* the search-time
reranker all default to OpenAI when you don't pass your own. Point all three at OpenRouter, or
replace them. The reranker is the one people miss: pass the other two and `Graphiti(...)` still
fails on construction with `Missing credentials ... OPENAI_API_KEY`.

**`invalid_json_schema ... 'additionalProperties' is required`.** OpenAI models behind OpenRouter
reject Graphiti's default structured-output request. Pass
`structured_output_mode="json_object"` to `OpenAIGenericClient`. This one is not in Graphiti's docs.

**Docker is required** for FalkorDB (`docker compose up -d`). If Docker isn't an option on your
machine, tell us early.

**Python 3.11+**, but you don't have to install it: `uv sync` fetches the right version.

**`No module named 'httpx'`** means your checkout is older than the fix; pull, then `uv sync`.
`uv run pytest` includes a test that catches this.

## What we are grading

| Weight | What we look at |
|---|---|
| 30% | **Extraction quality.** Right companies, right numbers, right direction (who bought whom), nothing invented. Decoy documents produce nothing. |
| 20% | **The graph.** Do the entity and relationship types fit the questions? Is the same company one node and not four? Are dates on the facts? |
| 20% | **The answers.** Correct, cited, and genuinely derived from the graph. |
| 20% | **Engineering.** Tests worth having, code we can follow, one command to run it, honest handling of failures. |
| 10% | **Judgement.** `NOTES.md`: where it is weak, what you would do next, what it cost. |

Things that lose marks fast: answers that don't cite documents, invented figures, a README that
claims more than the code does, tests that assert nothing, secrets committed.

**If you run short on time**, cut scope, not honesty: fewer document types handled, but say so in
`NOTES.md`. A small pipeline that works end to end beats a large one that doesn't run.

## Submitting

Push to a private GitHub repo and add the reviewer we name in the email, or send a zip (no
`.venv`, no `.env`). Include `NOTES.md`. Tell us roughly how long you spent.

## Hints, so you spend your time on the interesting part

- Graphiti's API is `async`, and every episode you add costs an LLM call (or several): expect
  seconds per document, not milliseconds. Load once, then query.
- Give Graphiti the **date the thing happened**, not the time you ran your script. Its whole point is
  time: facts that were true, and facts that got replaced.
- Decide early whether one company's data is one graph or all companies share one. Both are
  defensible; say why you chose yours.
- Its extraction is not magic. If you hand it raw filing text and hope, you will get a mush of
  entities. Think about what you send it and how you type it.

## About the data

These are real, public filings and headlines, collected in September 2026 for this exercise. They
are included for evaluation only. Each row in `data/manifest.json` carries the source URL so you can
check anything against the original.
