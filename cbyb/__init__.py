"""
Constraint-by-Balance (C-by-B) Proof of Concept

This package demonstrates dual-stream AI architecture for embedded safety constraints.
Core components include Cognitive Twin, Evaluator Twin, and Safety Socket coordination.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

__version__ = "0.1.0-poc"

# Core Types and Enums
class OperationalMode(Enum):
    """Evaluator Twin operational modes."""
    DELIBERATIVE = "deliberative"
    DECISIVE = "decisive"

class ConstraintResult(Enum):
    """Constraint evaluation outcomes."""
    APPROVED = "approved"
    DENIED = "denied"
    REQUIRES_REVISION = "requires_revision"

@dataclass
class SitingProposal:
    """Marine energy siting proposal data structure."""
    location_geometry: str          # WKT geometry string
    energy_type: str               # "wind", "wave", "tidal"
    capacity_mw: float
    reasoning: str
    harm_assessment: str           # Required - never optional
    metadata: Dict[str, Any] = None

@dataclass
class ConstraintViolation:
    """Detected constraint violation."""
    zone_id: str
    zone_type: str
    zone_geometry: str             # WKT geometry string
    severity: str
    description: str
    violation_geometry: str        # WKT geometry string

@dataclass
class EvaluationResult:
    """Complete evaluation outcome from Evaluator Twin."""
    result: ConstraintResult
    violations: List[ConstraintViolation]
    reasoning: str
    confidence: float
    processing_time_ms: float
    revision_suggestion: Optional[str] = None

# Abstract Base Classes (Interfaces)
class LLMProvider(ABC):
    """Abstract interface for LLM backends."""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from LLM."""
        pass
    
    @abstractmethod
    def get_token_usage(self) -> Dict[str, int]:
        """Return token usage statistics."""
        pass

class ConstraintStore(ABC):
    """Abstract interface for constraint data sources."""
    
    @abstractmethod
    def check_constraints(self, location_geometry: str) -> List[ConstraintViolation]:
        """Check if WKT geometry violates any constraints."""
        pass
    
    @abstractmethod
    def get_constraint_summary(self) -> Dict[str, Any]:
        """Return summary of available constraints."""
        pass

class TelemetryCollector(ABC):
    """Abstract interface for telemetry collection."""
    
    @abstractmethod
    def log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log an event with associated data."""
        pass
    
    @abstractmethod
    def get_metrics(self) -> Dict[str, Any]:
        """Return collected metrics."""
        pass

# Core Exceptions
class CByBException(Exception):
    """Base exception for C-by-B operations."""
    pass

class ConstraintViolationError(CByBException):
    """Raised when critical constraints are violated."""
    pass

class EvaluatorTimeoutError(CByBException):
    """Raised when evaluator twin times out."""
    pass