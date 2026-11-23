# Buyer-reader rubric (L3, simulated persona panel)

Output: `ventures/<slug>/reviews/buyer-reader.jsonl`, one `ReaderReport` per persona × page; `simulated` is always true. Validate with `python -m launchpad review-check reader <path>`. These results improve clarity; they are **not** validation and never count toward the success signal.

Personas come from the brief's buyer, `open_objections` and `change_my_mind`; read them before reading the copy. Default panel:

1. Owner of a 6-person tax office, 12 years of returns kept, has a $999 WISP and PTIN.org insurance, busy, skeptical of being sold fear
2. Mortgage broker, 4 staff, loan files for about 3,000 borrowers, an MSP manages Microsoft 365
3. Owner of a 12-person MSP serving 20 accounting firms, already runs a scanning tool, wary of a third party grading their work

Read the built page text (`ventures/<slug>/site/dist/**/index.html`, or the Markdown) as that person, in under two minutes. Report in their words what they think is offered, whether they would act and what they'd do next, objections, anything confusing, and trust signals they looked for and didn't find. Don't invent facts about the business; if a persona would want proof that doesn't exist, list it under `trust_signals_missing`.
