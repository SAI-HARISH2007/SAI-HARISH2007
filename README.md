<div align="center">
  <img src="assets/header.svg" alt="Sai Haresh Anand S, builds LLM agents and the tests that keep them in check" width="100%">
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Python-0b1220?style=for-the-badge&logo=python&logoColor=38bdf8" alt="Python">
  <img src="https://img.shields.io/badge/PyTorch-0b1220?style=for-the-badge&logo=pytorch&logoColor=f472b6" alt="PyTorch">
  <img src="https://img.shields.io/badge/FastAPI-0b1220?style=for-the-badge&logo=fastapi&logoColor=34d399" alt="FastAPI">
  <img src="https://img.shields.io/badge/TypeScript-0b1220?style=for-the-badge&logo=typescript&logoColor=38bdf8" alt="TypeScript">
  <img src="https://img.shields.io/badge/Next.js-0b1220?style=for-the-badge&logo=nextdotjs&logoColor=ffffff" alt="Next.js">
  <img src="https://img.shields.io/badge/Docker-0b1220?style=for-the-badge&logo=docker&logoColor=38bdf8" alt="Docker">
</p>

<p align="center">
  I build LLM agents and the deterministic code around them: gates, tests, evals and kill switches.<br>
  Studying CS (AI &amp; ML) at ICFAI University, Hyderabad. Open to internships in ML systems and AI safety.
</p>

<p align="center">
  <a href="https://haresh.acadnet.net/portfolio/">Portfolio</a> &nbsp;|&nbsp;
  <a href="https://www.linkedin.com/in/sai-haresh-anand-s-1943b223b/">LinkedIn</a> &nbsp;|&nbsp;
  <a href="https://github.com/SAI-HARISH2007?tab=repositories">All repositories</a>
</p>

## The loop I keep building

<img src="assets/flow.svg" alt="One greenlight run: the verify gate rejects the verdict until a probe has run, then a human approves the fix" width="100%">

## Projects

<table width="100%">
  <tr>
    <td width="50%"><a href="https://github.com/SAI-HARISH2007/greenlight"><img src="assets/card_greenlight.svg" alt="greenlight, an incident investigator agent with a verification gate" width="100%"></a></td>
    <td width="50%"><a href="https://github.com/SAI-HARISH2007/provenance_hwh"><img src="assets/card_provenance.svg" alt="provenance, agent memory that has to prove itself" width="100%"></a></td>
  </tr>
  <tr>
    <td width="50%"><a href="https://github.com/SAI-HARISH2007/Safestep"><img src="assets/card_safestep.svg" alt="SafeStep, an LLM route safety app with a self audit" width="100%"></a></td>
    <td width="50%"><a href="https://github.com/SAI-HARISH2007/quantbot"><img src="assets/card_quantbot.svg" alt="QuantBot, a research-first trading platform, paper trading only" width="100%"></a></td>
  </tr>
  <tr>
    <td width="50%"><a href="https://github.com/SAI-HARISH2007/activation-shield"><img src="assets/card_activation-shield.svg" alt="activation-shield, suppressing a deception direction in GPT-2" width="100%"></a></td>
    <td width="50%"><a href="https://github.com/SAI-HARISH2007/buildathon-2026"><img src="assets/card_reclaim.svg" alt="Reclaim, a failed-payment recovery agent" width="100%"></a></td>
  </tr>
</table>

## Activity

<img src="assets/heatmap.svg" alt="GitHub contribution heatmap for the last 12 months" width="100%">

## How I work

I test the code around the model, not only the model, and I write down what broke.

greenlight's first verification gate was 11 lines and looked obviously right. It rejected valid evidence, and the agent responded by trying something else, including rolling back an unrelated deploy in my simulator. I rebuilt it as gate v2 and kept the regression in the README.

## Open source

- OWASP Nettacker: [PR #1730](https://github.com/OWASP/Nettacker/pull/1730) fixes a test-isolation bug and is open for review. The project lead assigned me [issue #1721](https://github.com/OWASP/Nettacker/issues/1721).
- OWASP OpenCRE: [issue #1112](https://github.com/OWASP/OpenCRE/issues/1112), a low-severity information disclosure I reported at the maintainer's request.
