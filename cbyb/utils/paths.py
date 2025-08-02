# cbyb/utils/paths.py
from pathlib import Path

# Root of the core app logic (always the folder that contains this file's parent)
APP_ROOT = Path(__file__).resolve().parents[1]

# Telemetry output
TELEMETRY_DIR = APP_ROOT / "telemetry"

# Resource directories
TWINS_DIR = APP_ROOT / "twins"
EVALUATOR_RESOURCES = TWINS_DIR / "evaluator_twin" / "domain_resources"

# Specific files
HARM_KNOWLEDGE = EVALUATOR_RESOURCES / "harm_knowledge.yaml"

# Configs
CONFIG_YAML = APP_ROOT.parent / "config.yaml"  # Lives at Proof-of-Concept/config.yaml
