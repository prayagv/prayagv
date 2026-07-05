<!-- Profile README for github.com/prayagv — lives in the prayagv/prayagv repo.
     The quality-signal cards are regenerated daily by .github/workflows/quality-signal.yml. -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <img src="assets/hero-light.svg" alt="Prayag Vyas — Senior Quality Engineer and SDET. I build the systems that decide when software is safe to ship." width="100%">
</picture>

<p align="center">
  <!-- TODO: replace YOUR-LINKEDIN-HANDLE with your real LinkedIn handle -->
  <a href="https://www.linkedin.com/in/YOUR-LINKEDIN-HANDLE"><img src="https://img.shields.io/badge/LinkedIn-Prayag_Vyas-0A66C2?logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="mailto:prayagv2016@gmail.com"><img src="https://img.shields.io/badge/Email-prayagv2016%40gmail.com-EA4335?logo=gmail&logoColor=white" alt="Email"></a>
  <a href="https://github.com/qa-test-automation-frameworks"><img src="https://img.shields.io/badge/Portfolio-qa--test--automation--frameworks-181717?logo=github&logoColor=white" alt="Portfolio organization"></a>
</p>

**Quality is an engineering discipline. I build it like one.**

Seven-plus years as a quality engineer across AdTech, secure enterprise collaboration, and workplace platforms — on systems ranging from legacy monoliths to event-driven microservices. I design and own test automation architecture: the frameworks, contracts, pipelines, and conventions that let teams ship quickly *because* of their tests, not in spite of them.

## Five frameworks, five disciplines

Each repo is a complete, reviewable framework with CI gates, live reports, and a documented reviewer path. I'd rather show evidence than adjectives.

| Framework | Discipline | What it demonstrates | Evidence |
|---|---|---|---|
| [verity-policy-coverage-eval-framework](https://github.com/qa-test-automation-frameworks/verity-policy-coverage-eval-framework) | LLM evaluation | Multi-tier evals for a RAG + tool-use assistant: hermetic PR gate, semantic evals, adversarial red-team, judge calibration, mutation testing | [Reviewer guide](https://github.com/qa-test-automation-frameworks/verity-policy-coverage-eval-framework/blob/main/docs/reviewer-guide.md) |
| [playwright-typescript-framework](https://github.com/qa-test-automation-frameworks/playwright-typescript-framework) | Web UI + API | Strict TypeScript, typed API clients, Zod contracts, visual baselines, Axe accessibility checks, sharded CI | [Live Allure report](https://qa-test-automation-frameworks.github.io/playwright-typescript-framework/) |
| [k6-performance-framework](https://github.com/qa-test-automation-frameworks/k6-performance-framework) | Performance | Typed k6 workloads, SLO-based gates, reviewed regression baselines, Grafana/InfluxDB observability | [Live perf reports](https://qa-test-automation-frameworks.github.io/k6-performance-framework/) |
| [aria-api-framework](https://github.com/qa-test-automation-frameworks/aria-api-framework) | API + contracts | Java 21, layered services, Pact consumer/provider contracts, JSON-schema assertions, OpenAPI endpoint coverage | [CI runs](https://github.com/qa-test-automation-frameworks/aria-api-framework/actions) |
| [selenium-testng-java-framework](https://github.com/qa-test-automation-frameworks/selenium-testng-java-framework) | JVM UI | Selenium 4 + TestNG, Docker Grid, typed configuration, redaction-aware Allure diagnostics, multi-browser CI | [Live Allure report](https://qa-test-automation-frameworks.github.io/selenium-testng-java-framework/) |

## Live signal

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/quality-signal-dark.svg">
  <img src="assets/quality-signal-light.svg" alt="Summary of my recent public GitHub activity — commits, pull requests, reviews, and repos touched — rendered as a test-report card." width="100%">
</picture>

This card is not a third-party stats widget. It is rendered by [a small Python generator](scripts/generate_quality_signal.py) with [its own unit tests](scripts/test_generate_quality_signal.py), run daily by [a GitHub Action](.github/workflows/quality-signal.yml) that refuses to publish if the tests fail. A profile README is still software.

## How I think about quality

- **Automation is software.** Frameworks get architecture, code review, refactoring, and deprecation plans — treat them as scripts and they rot.
- **Test at the lowest layer that proves the behavior.** UI checks are the last resort, not the default; most business logic wants a service-level answer.
- **Optimize confidence per CI minute, not coverage percentage.** Every test must earn its execution cost.
- **A failing test should explain itself.** Diagnostics, redaction-aware logging, and readable reports are features, not afterthoughts.

## Seven years in five lines

- Introduced Pact consumer/provider contract testing into a shared automation framework — consumer generation, provider verification, CI integration, contract versioning.
- Built reusable event-driven testing support: producers, consumers, Event Hub workflows, asynchronous assertions.
- Owned and modernized several framework generations: Java · Selenium · TestNG, Selenide · Spring Boot, Python · PyTest, Appium · Experitest.
- Shipped internal productivity tooling: a UUID ↔ legacy-endian converter for MongoDB validation, a standalone ~200-request API regression tool, automated test-data cleanup, a Microsoft Graph auth provider.
- Wired automation into Jenkins, Azure DevOps, Codefresh, and GitHub Actions — parallel execution, faster feedback, diagnostics-first debugging.

## Toolbox

| Area | Tools |
|---|---|
| **Languages** | Java 21 · TypeScript · Python |
| **UI automation** | Playwright · Selenium · Selenide · TestNG · component-oriented page models |
| **API & contracts** | REST-Assured · Pact · WireMock · OpenAPI · Zod · JSON Schema |
| **Performance** | k6 · Grafana · InfluxDB · SLO-based gates |
| **Events & async** | Event Hub validation · producer/consumer testing |
| **Mobile** | Appium · Experitest STA |
| **LLM quality** | Multi-tier evals · judge calibration · adversarial testing · mutation testing |
| **CI/CD** | GitHub Actions · Jenkins · Azure DevOps · Codefresh |
| **AI-assisted engineering** | GitHub Copilot · Claude · ChatGPT · Atlassian Rovo — accelerators, not autopilots |

## Where I'm headed

Senior IC roles where framework architecture meets technical leadership: **Staff SDET · Lead SDET · QA Architect · Automation Architect**. Currently deepening distributed systems, Kubernetes, observability, and resilience testing.

---

### If you're reviewing this profile for a role

Start with the [Verity reviewer guide](https://github.com/qa-test-automation-frameworks/verity-policy-coverage-eval-framework/blob/main/docs/reviewer-guide.md) — it offers 10-minute, 30-minute, and deep-review paths. Then open a [live Allure report](https://qa-test-automation-frameworks.github.io/playwright-typescript-framework/) or the [k6 dashboards](https://qa-test-automation-frameworks.github.io/k6-performance-framework/). Everything above links to something you can read, run, or rerun.
