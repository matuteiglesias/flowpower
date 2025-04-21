# ⚡ FlowPower

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![License: BSL-1.1](https://img.shields.io/badge/license-BSL--1.1-blue)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-96%25-success)

> **FlowPower** is a lean, extensible runner + tracer for PromptFlow YAML.  
> Built to power local flows, trace pipelines, and serve as the open-core behind intelligent AI agents.

---

### 🔥 Features

- ⚡ Ultra-fast CLI for running and tracing promptflow YAMLs
- 🧩 Modular architecture (core + API + UI coming soon)
- 🛠️ Ideal for power users, agent builders, and toolchain integrators
- 🌐 Community-driven templates & pro packs in progress

---

### 🧱 Studio-Grade Stack

- `flowpower-core`: MIT/BSL-licensed CLI + SDK
- `flowpower-api`: FastAPI orchestration server _(coming soon)_
- `flowpower-ui`: GUI frontend for editing and tracing flows _(coming soon)_

---

Absolutely — here’s a compact and polished **README CLI Quickstart** section tailored to your `fp` alias (PromptFlow CLI wrapper), showcasing the key capabilities you’ve mastered.

---

## 🧪 FlowPower CLI — Quickstart with `fp`

Install the Python module in your environment:

```bash
pip install -e ./src
```

> ✅ This enables the `promptflow` CLI — aliased here as `fp` for brevity.

---

### 🚀 Run Powerful Examples via CLI

Each of these examples demonstrates a unique aspect of PromptFlow’s capabilities:

---

#### 1. 🧠 **Autonomous Agent (Multi-tool LLM chain)**
Runs a lightweight AutoGPT-style agent with tools and reasoning steps.

```bash
fp flow test --flow ./flows/standard/autonomous-agent \
  --inputs goal="Build a weather app."
```

---

#### 2. 📐 **Maths to Code (LLM + code execution)**
Demonstrates prompt-based Python generation + safe execution.

```bash
fp flow test --flow ./flows/standard/maths-to-code \
  --inputs question="What is 3+3 in Python code?"
```

---

#### 3. 🔍 **Named Entity Recognition (Text cleansing pipeline)**
Showcases chained text extraction + post-processing.

```bash
fp flow test --flow ./flows/standard/named-entity-recognition \
  --inputs text="Barack Obama was born in Hawaii." entity_type="person"
```

---

#### 4. 🌍 **Web Classification (Multi-step pipeline + summarization)**
Full chain: fetch page → summarize → classify → convert output.

```bash
fp run create \
  --flow ./flows/standard/web-classification \
  --data ./flows/standard/web-classification/data.jsonl \
  --column-mapping url='${data.url}'
```

---

#### 5. 🌐 **Serve as API (Flask server + UI-ready)**
Turn a `.yaml` or `.prompty` into a live local HTTP endpoint:

```bash
fp flow serve --flow ./flows/standard/maths-to-code
```

> You’ll get a local URL like: [http://localhost:55805/score](http://localhost:55805/score)  
> Then test with:

```bash
curl -X POST http://localhost:55805/score \
  -H "Content-Type: application/json" \
  -d '{"question": "What is 5*12 in Python code?"}'
```

---

### 🔧 Dev Tips

- Use `fp flow test` for quick interactive checks.
- Use `fp run create` for batch runs with `.jsonl` files.
- Use `fp flow serve` to launch flows as local APIs.

---
