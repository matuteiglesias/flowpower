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

### 🚀 Quickstart

```bash
pip install flowpower-core
fp run run ./data/standard_flow/flow.dag.yaml --data ./data/input.json
