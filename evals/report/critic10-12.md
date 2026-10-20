Critics 10–12 (three fresh independent Claude Sonnet sub-agents, blind, own shuffles; mappings in critic10/11/12-mapping.json).
Each film: a 20-frame sheet from 1.0 s (no fade-from-black frame) + a moments sheet (HOOK 0.5–6.5 s, HERO −1…+5 s, END last 5 s), made with evals/sheet.py.
Averages of the eight rubric criteria:
| Film | Critic 10 | Critic 11 | Critic 12 | Mean |
|---|---|---|---|---|
| reference aurel | 3.25 | 3.38 | 3.25 | 3.29 |
| r7-aurel | 3.25 | 3.38 | 3.25 | 3.29 |
| r8-aurel | 3.13 | 3.13 | 3.25 | 3.17 |
| r7-quartile | 2.88 | 2.75 | 2.88 | 2.84 |
| r8-quartile | 2.88 | 2.63 | 3.13 | 2.88 |
| r7-larchwood | 3.25 | 3.50 | 3.38 | 3.38 |
| r8-larchwood | 3.50 | 3.63 | 3.50 | 3.54 |
| r7-medstat-real | 3.00 | 3.38 | 3.13 | 3.17 |
| r8-medstat-real | 3.25 | 3.38 | 3.13 | 3.25 |
Hook scores for the same five films (reference + round 7): old sheets (critics 7–9) mean 3.00, fixed sheets (critics 10–12) mean 2.93.
Hero scores, round 8: aurel 3/3/3, quartile 2/2/3, larchwood 3/3/3, medstat 3/3/3.
