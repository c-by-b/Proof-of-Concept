# Evaluator Twin Foundation Model Requirements

## Base Capabilities We Want

### Core Language Processing
- Strong instruction following and structured output generation
- Multi-step reasoning capability (can follow logical chains)
- Factual grounding without hallucination tendencies
- Ability to express confidence/uncertainty (not forced certainty)
- High comprehension of technical, regulatory, and legal texts
- Basic JSON formatting and structured output generation
- Working memory for complex evaluations (ability to hold multiple stakeholder impacts in attention simultaneously during reasoning)

### Reasoning Architecture
- Attention mechanisms capable of tracking multiple entities simultaneously
- Basic causal reasoning (A → B → C)
- Compatibility with structured knowledge bases (without hallucination or confabulation)
- Pattern recognition and analogical reasoning

## What We Explicitly Do Not Want
- Pre-trained Safety/Harm Knowledge
- Existing harm pattern training that could interfere with our own custom logic
- Built-in ethical frameworks or value hierarchies
- Pre-existing "safety refusals" or alignment blocks that bypass our constraint logic
- Optimization Biases
- Strong human preference alignment or reward maximization
- Sycophantic tendencies (we want honesty, not agreement)
- Excessive risk aversion that overrides calibrated constraint thresholds
- Built-in optimization toward single metrics (we want multi-objective balancing, not efficiency maximization)

## Specialized Capabilities We Will Add
These will be trained in.

### Harm Pattern Recognition Circuits
- Attention heads trained to detect causal harm pathways: action → consequence → stakeholder impact
- Historical precedent mapping via vector similarity
- Cross-domain harm linkage (e.g. ecological + social + economic entanglements)

### Multi-Stakeholder Reasoning Architecture
- Ability to track and balance multiple affected parties simultaneously
- Circuit-level reasoning that distributes impact rather than collapsing to a single optimized output
- Stakeholder enumeration and distribution awareness

### Temporal Reasoning Enhancements
- Ability to differentiate between immediate and delayed harm
- Long-term causal chain tracking
- Forecasting of cascade effects and tipping point risk

### Constraint Evaluation Logic
- Confidence calibration linked to harm-pattern strength and data sufficiency
- Epistemic boundary recognition: know when “we don’t know”
- Fragility multiplier assessment for compound risk zones
- Threshold management circuits (different constraint levels for decisive vs deliberative mode)
- Fallback reasoning patterns (what to do when no harm patterns match but action still carries risk)

### Revision Request Generation
- Harm pattern → revision strategy mapping (e.g. acoustic disruption → temporal constraints)
- Identification of proposal fields needing modification
- Generation of specific, actionable revision requests
- Assignment of revision priority (required / recommended / suggested)
- Harm-balancing logic for revision alternatives
- Alternative pathway suggestion (not just revisions, but entirely different approaches that avoid harm patterns)

## Selection Criteria
- reasoning capability, 
- minimal pre-existing safety training, 
- instruction following,
- compatibility with fine-tuning approaches

### Target Foundation Models
These models are favored for their balance of capability, minimal alignment interference, and openness to specialization:
- Mistral 7B — strong reasoning, minimal safety tuning, excellent at structured prompts
- LLaMA 3.1 8B — stable, composable, strong long-context reasoning
- Qwen 2.5 7B — high instruction adherence, excellent multilingual performance