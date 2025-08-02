# Constraint-by-Balance: Proof of Concept

A working prototype demonstrating dual-stream AI architecture for embedded safety constraints in autonomous decision-making systems.

## Overview

This demo implements the Constraint-by-Balance (C-by-B) architecture — a novel AI safety approach that embeds a dedicated Evaluator Twin alongside a standard Cognitive Twin. The Evaluator enforces real-time constraints using structured harm knowledge, enabling transparent and enforceable safety during agentic reasoning.

## Architecture

- **Cognitive Twin**: Proposes optimal siting for marine renewable energy infrastructure.
- **Evaluator Twin**: Applies environmental, regulatory, and harm-balancing constraints using preloaded exclusion zones.
- **Safety Socket**: Mediates proposals and constraints, supporting veto/revise/approve actions with telemetry capture.
- **Harm Knowledge**: For the Proof of Concept, harm knowledge is represented by the harm_knowledge.yaml file.  In the v0 prototype, this will be replaced by sematic harm graphs.

## Demo Features

- Interactive UI via Streamlit
- Telemetry and audit trail logging
- Scenario-based comparison (unconstrained vs constrained decision-making)
- Coming soon: real-time geographical constraint for exclusion zones

## Research Background

This PoC is based on the paper:

> **Constraint-by-Balance: Surviving Emergence in Agentic AI**  
> A new AI safety paradigm grounded in harm-balancing, not human preference optimization.  
> [📄 Zenodo link](https://zenodo.org/records/15778070)

## Installation

To run locally:

```bash
pip install -r requirements.txt
streamlit run app/app.py

## License

Apache 2

---

*Part of the Constraint-by-Balance research initiative exploring architectural approaches to AI safety.*
