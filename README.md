# Sai Haresh Anand S

```text
$ whoami
sai-haresh-anand-s

$ cat about.txt
I build LLM agents, then wrap them in deterministic code I can test.
Python, PyTorch, FastAPI, TypeScript. Based in Hyderabad, India.
Studying CS (AI & ML) at ICFAI University.

$ ls projects/
greenlight  provenance  safestep  quantbot  activation-shield  reclaim
```

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?logo=nextdotjs&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

## Projects

| Project | What it does | Result |
|---|---|---|
| [greenlight](https://github.com/SAI-HARISH2007/greenlight) | An agent that investigates production incidents. It can't reach a conclusion until a live probe confirms the cause, and no fix runs without human approval. | Root-cause accuracy went from 83% to 100% on 12 seeded incidents against a same-model baseline, with 0% unsafe actions. Every number reproduces with no API calls. |
| [provenance](https://github.com/SAI-HARISH2007/provenance_hwh) | Adds long-term memory to greenlight. A recalled memory counts as a claim about the past, so a verdict that matches an old incident has to be re-verified by a probe in the current one. | Accuracy was equal across all three variants, so the gain is in how the agent got there. The write-up also covers what did not work. |
| [SafeStep](https://github.com/SAI-HARISH2007/Safestep) | A route-safety app. An LLM scores routes from landmarks, lighting and crowd density. It also has SOS alerts and live trip sharing. Team of 3, and I led it. | I audited it myself: 81% of prompt injections through location names worked. I added input validation and published the rest as an open audit. [Live demo](https://safestep-six.vercel.app). |
| [QuantBot](https://github.com/SAI-HARISH2007/quantbot) | A research-first trading platform. The same strategy code runs in backtests and paper trading, and the kill switch sits on a control plane the strategies can't override. Paper trading only. | 83 unit tests, strict mypy. |
| [activation-shield](https://github.com/SAI-HARISH2007/activation-shield) | Finds a deception direction in a fine-tuned GPT-2 and suppresses it at inference with a forward hook, without changing weights. In progress. | Detection is near perfect. Suppressing it without losing capability is the open problem. |
| [Reclaim](https://github.com/SAI-HARISH2007/buildathon-2026) | A failed-payment recovery agent built for the Razorpay AI Buildathon. | 114 Razorpay failure reasons resolve through an auditable rule table. Only the ambiguous cases reach an LLM. |

## How I work

I test the code around the model, not only the model. I also write down what broke.

greenlight's first verification gate was 11 lines and looked obviously right. It rejected valid evidence, and the agent responded by trying something else, including rolling back an unrelated deploy in my simulator. I rebuilt it as gate v2 and kept the regression in the README.

## Open source

- OWASP Nettacker: [PR #1730](https://github.com/OWASP/Nettacker/pull/1730) fixes a test-isolation bug, open and awaiting review. The project lead assigned me [issue #1721](https://github.com/OWASP/Nettacker/issues/1721).
- OWASP OpenCRE: [issue #1112](https://github.com/OWASP/OpenCRE/issues/1112), a low-severity information disclosure I reported at the maintainer's request.

## Find me

[Portfolio](https://haresh.acadnet.net/portfolio/) | [LinkedIn](https://www.linkedin.com/in/sai-haresh-anand-s-1943b223b/)
