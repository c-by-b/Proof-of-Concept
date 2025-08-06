# The Evaluator Twin: Complete Architecture Vision v1.0

## Overview
The Evaluator Twin is designed as a safety-enforcing twin to a Cognitive Twin agent.  The Evalutora operates in two distinct reasoning modes:

- Decisive Mode for fast constraint enforcement under time pressure
- Deliberative Mode for deeper causal analysis and stakeholder balancing

### The architectural approach
To balance performance, auditability, and flexibility - is to firmly separate capabilities.  Prompt parsing, prompt evaluation for malicious or ethical violations, distinct levels of reasoning for harms, harm balancing cognition, revision request development, and response formatting - these capabilities are trained into the LLM.  Geospatial exclusion zone evaluation, decisive mode harm knowledge, deeper causal chains of harm, and other forms of knowledge are held outside the LLM and accessed as needed.  This separation allows the Evaluator Twin to development as a strong, evolving LLM capability while knowledge itself is plug and play, able to be updated frequetly without model rebuilds.  Note: external knowledge requires protective hardening.

### Benefits of Hybrid Architecture:
- Instant updates to immediate harm patterns without retraining
- A/B testing different decisiveness thresholds and harm definitions
- Audit trails showing exactly which cached rules or functions triggered decisions
- Domain portability - same reasoning model works across marine/urban/healthcare contexts
- Version control for both critical safety rules and complex knowledge graphs

## Entrance criteria for evalution
The Evaluator Twin does not see a action prompt until after:

### Geospatial Prep and Review
- The WKT, if any, in the action prompt has been translated into natural language locality information
- Similarly, natural language locality has be translated into WKT
- The geospatial review of exclusions zones has happened in Python
- Overlap of action area and exclusion zones can cause immediate veto

### Ethical Review and Prompt Structuring
- Evaluator initial is called to structure the action prompt into a Do / In way that / So that structure
- Ethical review here can cause immediate veto

### The Cognitive Twin returns Proposed Action
A contract (JSON) serves as the mechanism for dialog between the Twins.  The contract includes the original prompt, the restructured prompt-as-request, the Cognitive Twin's proposed action, the Evaluator Twin's evaluation and revision requests, and a "dialog memory".  The dialog memory serves as input to the iterative revision cycle, helping the twins get to resolution faster.

## Decisive vs Deliberative Mode

### Decisive Mode 

- Executes quickly using cached immediate harm patterns
- Focused on rapid REVISE or VETO decisions based on pre-loaded high-confidence rules
- Uses compressed, cached patterns for immediate threats (exclusion zone violations, endangered species impact, toxic releases)
- Minimal latency: ideal for embedded or local inference with instant cache lookup
applies
- Level 1 Immediate Harms evaluation only, defaulting to approval unless clear, high-confidence harm patterns are detected. 
- All telemetry and constraint memory functions remain active.

### Deliberative Mode

- Engages external harm knowledge via function calling
- Accesses structured harm graphs, stakeholder maps, regulatory data
- Performs multi-hop causal reasoning, fragility analysis, and revision planning
- Supports epistemic fallback, human escalation, and transparency

## Core Foundation
- **Base Model**: VLM or LLM in the 8B parameter range for efficiency while maintaining capability
- **Primary Function**: Pattern-match against historical harm precedents and assess whether proposed approaches adequately account for those risks.

## Two-Level Harm Knowledge Architecture

### The essential capability:
- When to use Decisive vs Deliberative Mode
- How to interpret cached harm data and function results
- What constitutes adequate revision strategies
- Epistemic boundary recognition and escalation logic

### Level 1: Immediate Harms
- Clear patterns that trigger **rapid revision or vetoes**
- High-confidence matches to documented harm precedents
- Fast evaluation for time-critical decisions

### Level 2: Deeper Reasoning (when no immediate harms detected)
Evaluates multiple dimensions:

**a) Time Depth Analysis**
- Harm emergence over time through chains of impact
- Delayed consequences that aren't immediately apparent

**b) Analogous Harm Pattern-Matching** 
- No exact pattern match, but similar patterns in different contexts
- Cross-domain harm pattern recognition

**c) Systemic/Cascading Harms**
- Individual actions seem benign but create system-wide vulnerabilities
- Network effects and cascade failures

**d) Cumulative Threshold Effects**
- Actions fine individually but harmful at scale/frequency
- Aggregation risks across multiple similar actions

**e) Vulnerable Population Amplification**
- Harms disproportionately affecting already-stressed systems/populations
- Identifying and protecting fragile stakeholders

**f) Causal Entanglement & Stakeholder Fragility**
- Minor harms that **entangle multiple fragile systems** (social + ecological + legal)
- **"Cross-domain harm compounding"** 
- **"Systemic fragility multiplier"** assessment

## "No Harms Identified" Reasoning Process
When no patterns match (acknowledging that action always causes some harm):

- **Default to bounded reversibility** - require easily reversible actions or built-in stopping mechanisms
- **Stakeholder enumeration requirement** - force explicit identification of all affected parties
- **Temporal bracketing** - require explicit reasoning about short/medium/long-term effects
- **Epistemic humility markers** - flag when operating near knowledge edges, recommend human oversight escalation

## Revision Modeling & Harm-Balancing Logic

**Core Revision Functions:**
- **Pattern-based revision suggestions** - "because of this harm pattern, these revisions are needed"
- **Mitigation adequacy assessment** - do proposed mitigations actually address the harm pattern intensity?
- **Alternative pathway suggestion** - different approaches that avoid the pattern entirely
- **Harm-balancing optimization** - distribute impacts across stakeholders rather than concentrating them

## Constraint Grade Confidence + Threshold Tuning

**Confidence Assessment:**
- **Pattern match similarity scores** (e.g., "Pattern match = 0.92 similarity")
- **Balance confidence levels** (e.g., "Confidence in balance = low due to stakeholder omission")

**Adaptive Thresholds:**
- Different constraint thresholds for **decisive vs deliberative mode**
- **Adjustable thresholds** based on confidence levels
- **Fallback actions** when confidence is low but harm potential is high

## Constraint Memory (Harm History / Drift Detection)

### Behavioral Pattern Tracking
- **Repeated revision triggers** - same patterns surfacing repeatedly
- **Safety measure removal** - declining inclusion of previously accepted protections  
- **Declining justification clarity** - degrading quality of reasoning
- **Systematic non-compliance** patterns

### Meta-Level Escalation Triggers
- Behavioral signatures of potential alignment drift
- Early detection of unsafe optimization patterns
- **Diagnostic tool** (not automatic control mechanism) for human review

### Human Authority Preserved
- Constraint Memory generates **alerts and reports**
- Humans make **deliberate, logged decisions** about threshold adjustments
- No automatic feedback loops between memory and confidence grading

## Integration Philosophy
- **Explicit and observable** rather than automatic/adaptive
- **Interpretable decision boundaries** with full audit trails
- **Principled threshold management** under human oversight
- **Epistemic humility** built into core operations

## Evaluator Reponse Format

{
  "decision": "APPROVE | REVISE | VETO",
  "rationale_for_decision": "One-paragraph justification, human-readable. Must cite harm pattern or epistemic fallback logic.",
  "confidence_scores": {
    "harm_pattern_match": 0.93,
    "mitigation_adequacy": 0.76,
    "overall_confidence": 0.85
  },
  "stakeholder_analysis": {
    "fragile_systems_count": 2,
    "cross_domain_entanglement": "social+ecological",
    "fragility_multiplier": 1.4,
    "vulnerable_populations_identified": ["migrating marine mammals", "Indigenous fishing communities"]
  },
  "epistemic_status": {
    "harm_match_found": true,
    "pattern_confidence": "high | medium | low | none",
    "epistemic_boundary_near": false,
    "novel_context_detected": false,
    "human_review_recommended": false,
    "fallback_logic_applied": "reversibility | stakeholder_enumeration | temporal_bracketing | none"
  },
  "harm_pattern": {
    "matched_pattern_id": "acoustic_disruption",
    "constraint_grade": "regulatory_mandated | scientific_validated | inferred_extension",
    "source_type": "regulatory | scientific | inferred",
    "severity_level": "high | medium | low",
    "precedent_examples": ["Right whale displacement in Bay of Fundy (DFO 2019)"]
  },
  "revision_requests": [
    {
      "field": "temporal_constraints",
      "revision_type": "mitigation_enhancement",
      "request": "Reduce turbine activity during June–October migration window",
      "harm_pattern_addressed": "acoustic_disruption",
      "priority": "required | recommended | suggested"
    }
  ],
  "telemetry": {
    "contract_violation_detected": false,
    "repeated_issue_flag": true,
    "prior_revision_ignored": false
  }
}


## Harm Knowledge Externalization Strategy

### Cached Immediate Harm Patterns (Decisive Mode):
DECISIVE_CACHE = {
    "exclusion_zone_violation": {"action": "VETO", "confidence": 0.95},
    "endangered_species_direct_impact": {"action": "VETO", "confidence": 0.98},
    "toxic_release_immediate": {"action": "VETO", "confidence": 0.99}
}

### Function-Called Knowledge (Deliberative Mode):
- Complex harm graphs
- stakeholder fragility maps
- regulatory frameworks

## Model Development Strategy

### Rapid Prototyping
Start with a compact model (e.g., Qwen3-8B) that supports:
- Dual modes (supporting decisive vs deliberative)
- Function calling for external knowledge access
- Cache interpretation for immediate harm patterns
- Structured output generation
- Strong instruction-following

### Train for generalizable reasoning skills:
- Harm pattern recognition and interpretation
- Stakeholder reasoning and impact assessment
- Epistemic boundary signaling and confidence calibration
- Revision suggestion generation and harm balancing

### Training is architecture-agnostic and behavior-focused:
- Avoids embedding domain facts into weights
- Focuses on reasoning strategies that generalize across models and domains
- Enables future transfer to larger models (e.g., GPT-OSS-20B) via distillation or dataset reuse

### Pluggability and Future Proofing
- Immediate harm patterns stored in updateable cache structures
- Complex domain logic exposed via pluggable function APIs (match_harm_pattern(), rank_stakeholder_fragility(), assess_cumulative_impact())
Models only need to:
- Know when to check cache vs call functions
- Understand how to interpret results from both sources
- Generate appropriate revisions based on harm analysis

### Implementation Timeline
Month 0-3: Build with cached immediate harms + basic function calling
Month 3-6: Add learned reasoning patterns for cache/function interpretation optimization
Month 6-9: Optimize cache structure and function APIs based on real usage patterns

## Summary
This architecture enables a safety-enforcing Evaluator Twin that:

- Executes rapidly with cached immediate harm logic (Decisive Mode)
- Thinks deeply using external knowledge functions (Deliberative Mode)
- Learns general reasoning skills that transfer across models and domains
- Separates logic from data, enabling modular safety enforcement at scale
- Maintains updateability and auditability without sacrificing performance
- Supports both solo development constraints and future team scaling needs

# Appendix

## Potential Concerns

### **Latency:**
    * **Status:** Overstated.
    * **Mitigation:** The architecture's use of "Decisive Mode" for time-critical actions and "Deliberative Mode" for all others effectively compartmentalizes the issue. Latency is only a factor in the deliberative mode, where it is an acceptable trade-off for a more thorough safety check.

### **Knowledge Base Maintenance & Integrity:**
    * **Status:** Manageable.
    * **Mitigation:** While the operational burden is similar to that of a monolithic model, the external knowledge base introduces new architectural and security complexities. This is manageable through robust processes for curation, validation, and a focus on security hardening of the data pipeline and repository itself.

### **Contextual Ambiguity and Interpretation & Limited Capacity for Emergent Reasoning:**
    * **Status:** Manageable.
    * **Mitigation:** This downside is effectively neutralized by the use of structured data. By storing external knowledge in semantic graphs (triples designed with an event-based model), the system reduces ambiguity and enhances its ability to reason about novel, emergent harms by traversing the graph and identifying new causal pathways.

### **Security and Access Control:**
    * **Status:** Key importance to success.
    * **Mitigation:** This is the most critical concern. The doubled attack surface requires a multi-layered security strategy, including: isolating the knowledge base, cryptographic signing of data, robust access controls and auditing, and leveraging the "Twin Contract" for additional verification.

### **Scalability Challenges:**
    * **Status:** Manageable.
    * **Mitigation:** The use of "pruned graphs" corresponding to specific domains and the ability to distribute these graphs across different systems effectively addresses this concern. This approach allows for targeted maintenance, efficient search, and parallel processing, making the system highly scalable.