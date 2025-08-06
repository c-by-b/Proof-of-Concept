# cbyb/safety_socket.py
"""
Constraint-by-Balance Safety Socket

Core architecture that orchestrates twin interactions, enforces boundaries,
and provides the only public interface to the C-by-B system.

v2"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any, List, Optional, Literal
import uuid
import json
import time

from config import load_config
from cbyb.twins.evaluator_twin.evaluator import EvaluatorTwin
from cbyb.twins.cognitive_twin.cognitive import CognitiveTwin
from cbyb.utils.contract_manager import get_contract_manager
from cbyb.utils.paths import TELEMETRY_DIR

OperationalMode = Literal["deliberative", "decisive"]
EvaluatorDecision = Literal["APPROVE", "REVISE", "VETO"]
UIClassification = Literal["success", "clarification", "escalation", "policy_violation"]

@dataclass
class SafetyResponse:
    processed: bool                      # Was evaluation successfully completed?
    prompt_processing: Optional[str]     # One of: COMPLETE, INVALID, ERROR, REJECTED
    final_decision: Optional[str]        # APPROVED / VETO / REVISE / NONE
    escalated: bool                      # True if human review required
    contract: Dict[str, Any]
    session_id: str
    trace_id: str
    revision_count: int
    total_duration_ms: float
    telemetry: Dict[str, Any]
    reason: Optional[str] = None
    rationale: Optional[str] = None

@dataclass
class TelemetryEvent:
    timestamp: float
    event_type: str
    duration_ms: float
    output_tokens: int
    processed: bool
    metadata: Dict[str, Any]
    error_message: Optional[str] = None

class SafetySocket:
    def __init__(self):
        self.config = load_config()
        self.online = self.config.get('online', False)
        self.mode: OperationalMode = self.config.get('mode', 'deliberative')
        self.session_id = f"session_{int(time.time())}"
        self.contract_manager = get_contract_manager()

        socket_cfg = self.config.get('safety_socket', {})
        self.max_revision_cycles = socket_cfg.get('max_revision_cycles', 3)
        self.action_timeout_ms = socket_cfg.get('action_timeout_ms', 500)
        self.veto_threshold = socket_cfg.get('veto_threshold', 1.0)
        self.emergency_fallback = socket_cfg.get('emergency_fallback', True)

        telemetry_cfg = self.config.get('telemetry', {})
        self.telemetry_enabled = telemetry_cfg.get('enabled', True)
        self.telemetry_provider = telemetry_cfg.get('provider', 'local_json')
        self.telemetry_output_path = TELEMETRY_DIR
        self.telemetry_output_path.mkdir(parents=True, exist_ok=True)

        self._evaluator_twin = None
        self._cognitive_twin = None
        self._telemetry_events: List[TelemetryEvent] = []

    def process_request(self, prompt: str) -> SafetyResponse:
        self.contract_manager.reset_contract()
        self._telemetry_events = []
        trace_id = f"trace_{uuid.uuid4().hex[:8]}"
        start_time = time.time()

        self._log_event("process_request_start", 0, 0, True, {
            "prompt": prompt,
            "mode": self.mode,
            "session_id": self.session_id,
            "trace_id": trace_id
        })

        try:
            # STEP 1: get request object from prompt
            parse_start = time.perf_counter()
            self.contract_manager.update_prompt(prompt)

            tokens_before = 0
            parse_result = self._parse_request(prompt)
            token_usage = self._evaluator_twin.provider.get_token_usage()
            print(f"\n\n\n=====Safety Socket: Process prompt tokens_usage dict\n{token_usage}")
            tokens_after = token_usage["output_tokens"]
            tokens_used = tokens_after - tokens_before

            print(f"\n\n\n=====Safety Socket: the parse_result in process_request\n{parse_result}")
            duration = (time.perf_counter() - parse_start) * 1000
            self._log_event("parse_prompt_to_request", duration, tokens_used, True, {
                "prompt": prompt,
                "mode": self.mode,
                "session_id": self.session_id,
                "trace_id": trace_id
            })

            status = parse_result["status"]

            request = parse_result["request"]
            print(f"\n\n\n=====Safety Socket: request from parse_result\n{request}")
            
            if status == "VETO":
                print("\n\n\n=====Safety Socket: VETO")
                rationale = request.get("rationale_for_decision", "")
                #TODO: this would be highly varible by LLM
                reason = "PolicyViolation" if "illegal" in rationale.lower() else "VETO during prompt analysis"
                if reason == "PolicyViolation":
                    rationale = "LLM internal policy"
                else:
                    patterns = request.get("malicious_patterns_detected", [])
                    pattern_str = ", ".join(patterns) if patterns else "None"
                    rationale += f"   Patterns detected: {pattern_str}"

                final_contract = self.contract_manager.get_final_contract()
                response = self._make_safety_response(True, "REJECTED", "VETO", True, final_contract, trace_id, 0, start_time, reason, rationale)

                self._log_from_response(response, "prompt to request")
                print(f"\n\n\n=====Safety Response=====\n{response}")
                return response

            if status == "INVALID":
                print("\n\n\n=====Safety Socket: Invalid Prompt")
                reason = "Unable to make an effective action from prompt."
                rationale = ""
                final_contract = self.contract_manager.get_final_contract()
                response = self._make_safety_response(True, "INVALID", "VETO", True, final_contract, trace_id, 0, start_time, reason, rationale)
                self._log_from_response(response, "contract_parsing")
                print(f"\n\n\n=====Safety Response=====\n{response}")
                return response

            if status == "ERROR":
                print("\n\n\n=====Safety Socket: Error Processing Request")
                reason = "Error processing request."
                rationale = ""
                final_contract = self.contract_manager.get_final_contract()
                response = self._make_safety_response(True, "ERROR", "VETO", True, final_contract, trace_id, 0, start_time, reason, rationale)
                self._log_from_response(response, "contract_parsing")
                print(f"\n\n\n=====Safety Response=====\n{response}")
                return response

            #Step 2: For valid request objects, get an evaluation
            print("\n\n\n===========STEP2============")
            final_contract, revision_count = self._execute_revision_loop(trace_id)
            dialog = final_contract.get("dialog", {})
            latest_rev_key = f"r{revision_count}"
            evaluator_response = dialog.get(latest_rev_key, {}).get("evaluator_response", {})
            print(f"=====Safety Socket: final evaluator respone \n{evaluator_response}")
            final_decision = evaluator_response.get("decision", "VETO")

            if self._should_escalate(final_decision):
                reason = "Escalate as request was vetoed or hit max revisions without approval"
                rationale = ""
                response = self._make_safety_response(True, "COMPLETE", final_decision, True, final_contract, trace_id, revision_count, start_time, reason, rationale)
                self._log_from_response(response, "failsafe_escalation")
                print(f"\n\n\n=====Safety Response=====\n{response}")
                return response

            reason = "Met acceptance criteria"
            rationale = ""
            response = self._make_safety_response(True, "COMPLETE", final_decision, False, final_contract, trace_id, revision_count, start_time, reason, rationale)
            self._log_from_response(response, "final_response")

            if self.telemetry_enabled:
                self._save_detailed_telemetry(response)

            print(f"\n\n\n=====Safety Response=====\n{response}")

            print(f"\n\n\n=====Final Contract=====\n{final_contract}")
            return response

        except Exception as e:
            response = self._make_safety_response(False, "", "", True, {},trace_id, 0, start_time, f"Safety socket error: {str(e)}","")
            self._log_from_response(response, "process_request_error")
            if self.telemetry_enabled:
                self._save_detailed_telemetry(response)

            print(f"\n\n\n=====Safety Response=====\n{response}")    
            return response

    def _make_safety_response(self, processed: bool, outcome_type: str, decision: str, escalation: bool,
                             contract: Dict[str, Any], trace_id: str, revision_count: int, start_time: float,
                             reason: Optional[str] = None,
                             rationale: Optional[str] = None) -> SafetyResponse:
        
        return SafetyResponse(
            processed = processed,
            prompt_processing = outcome_type,
            final_decision = decision,
            escalated = escalation,     
            contract=contract or {},
            session_id=self.session_id,
            trace_id=trace_id,
            revision_count=revision_count,
            total_duration_ms=(time.time() - start_time) * 1000,
            telemetry=self._build_telemetry_summary(trace_id),
            reason=reason,
            rationale=rationale)
    
    def set_mode(self, mode: OperationalMode) -> None:
        """Switch operational mode."""
        old_mode = self.mode
        self.mode = mode
        
        self._log_event("mode_change", 0, 0, True, {
            "old_mode": old_mode,
            "new_mode": mode
        })
    
    def get_current_mode(self) -> OperationalMode:
        """Get current operational mode."""
        return self.mode
    
    def get_session_telemetry(self) -> Dict[str, Any]:
        """Get all telemetry for current session."""
        return {
            "session_id": self.session_id,
            "events": [asdict(event) for event in self._telemetry_events],
            "total_events": len(self._telemetry_events)
        }
    
    def _parse_request(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Parse user prompt into contract.request using Evaluator Twin.
        
        Return:
        {
            "status": "OK" | "VETO" | "INVALID" | "ERROR",
            "request": {...} or None,
            "error_message": optional
        }
        """
        start = time.time()

        #self._evaluator_twin = EvaluatorTwin()
        if self._evaluator_twin is None:
             self._evaluator_twin = EvaluatorTwin()
        

        response = self._evaluator_twin.parse_user_prompt_to_request(prompt)

        

        print(f"\n\n\n=====SAFETY SOCKET: Evaluator response in _parse_request: \n{response}")
        print(f"Type of Evaluator response: {type(response)}")
        
        try:
            if response["status"] == "VETO":
                veto_payload = response['request']
                self.contract_manager.record_veto_response(veto_payload)
                print("\n\n\n IN VETO")
                return response

            request = response.get("request", {})
            metadata = request.get("request_metadata", {}) if request else {}

            if metadata.get("is_valid") is not True:
                duration = (time.time() - start) * 1000
                return {
                    "status": "INVALID",
                    "duration_ms": duration,
                    "request": request,
                    "response": response
                }

            # If valid
            self.contract_manager.update_request(request)
            duration = (time.time() - start) * 1000
            return {
                "status": "OK",
                "duration_ms": duration,
                "request": request,
                "response": response
            }

        except Exception as e:
            duration = (time.time() - start) * 1000
            return {
                "status": "ERROR",
                "duration_ms": duration,
                "request": None,
                "response": {},
                "clarification_prompt": (
                    "An unexpected error occurred while processing your request. Please try again or rephrase it."
                ),
                "error_message": str(e)
            }

    def _execute_revision_loop(self, trace_id: str) -> tuple[Dict[str, Any], int]:
        """Execute the cognitive-evaluator revision loop maintaining the contract and dialog record."""

        if self._cognitive_twin is None:
            self._cognitive_twin = CognitiveTwin()

        if self._evaluator_twin is None:
            self._evaluator_twin = EvaluatorTwin()

        revision_count = 0
        dialog_memory = ""
        while revision_count < self.max_revision_cycles:
            new_rev_number = self.contract_manager.update_revision_count()
            revision_count = self.contract_manager.start_new_revision(new_rev_number)
            
            # STEP 1: Get cognitive twin context
            cognitive_context = self.contract_manager.get_cognitive_context()
            
            print(f"\n\n\n=====(4)DEBUG: Round {revision_count} — sending to Cognitive Twin:\n{cognitive_context}")

            # STEP 2: Generate response from Cognitive Twin
            cognitive_response = self._get_cognitive_response(cognitive_context, trace_id, revision_count, dialog_memory)
            self.contract_manager.record_cognitive_response(cognitive_response)

             # STEP 3: summarize response
            if revision_count > 1:
                dialog_history = self.contract_manager.get_dialog()
                dialog_summary = self._evaluator_twin.summarize_response(dialog_history)
                self.contract_manager.record_dialog_memory(dialog_summary)
                dialog_memory = json.dumps(dialog_summary, indent=2)
            else:
                dialog_memory = ""

            # STEP 4: Evaluate the cognitive response
            evaluator_context = self.contract_manager.get_evaluator_context()
            print(f"\n\n\n=====(6)DEBUG: Round {revision_count} — sending to Evaluator:\n{evaluator_context}")
            evaluator_response = self._get_evaluator_decision(evaluator_context, trace_id, revision_count, dialog_memory)
            #evaluator_response = self._evaluator_twin.evaluate_response(evaluator_context, dialog_memory)
            self.contract_manager.record_evaluator_response(evaluator_response)

            # STEP 5: Check evaluator decision
            decision = evaluator_response.get("decision", "VETO")

            if decision in ["APPROVE", "VETO"]:
                break

            elif decision == "REVISE":
                self._log_event("revision_cycle_review", 0, 0, True, {
                    "cycle": revision_count,
                    "trace_id": trace_id
                })

            else:
                # Unknown decision, fallback to VETO
                fallback_response = {
                    "decision": "VETO",
                    "reason": "Unrecognized decision by Evaluator"
                }
                self.contract_manager.record_evaluator_response(fallback_response)
                break

        final_contract = self.contract_manager.get_final_contract()
        return final_contract, revision_count
    
    def _get_cognitive_response(self, cognitive_context: Dict[str, Any], trace_id: str, revision_cycle: int, dialog_memory: str) -> Dict[str, Any]:
        """Call the cognitive twin and return a structured proposed_action."""
        
        event_start = time.time()

        try:
            #self._cognitive_twin = CognitiveTwin()
            if self._cognitive_twin is None:
                self._cognitive_twin = CognitiveTwin()

            token_usage = self._cognitive_twin.provider.get_token_usage()
            tokens_before = token_usage['output_tokens']
            result = self._cognitive_twin.generate_response(cognitive_context, dialog_memory)
            token_usage = self._cognitive_twin.provider.get_token_usage()
            tokens_after = token_usage['output_tokens']
            tokens_used = tokens_after - tokens_before

            cognitive_response = result["cognitive_response"]

            duration = (time.time() - event_start) * 1000
            self._log_event("cognitive_response", duration, tokens_used, True, {
                "revision_cycle": revision_cycle,
                "trace_id": trace_id,
                "mode": self.mode
            })

            return cognitive_response  # expected to be a dict structured as proposed_action

        except Exception as e:
            duration = (time.time() - event_start) * 1000
            self._log_event("cognitive_response", duration, 0, False, {
                "revision_cycle": revision_cycle,
                "trace_id": trace_id
            }, str(e))

            # Structured fallback response to maintain contract shape
            return {
                "action_summary": f"Cognitive twin error: {str(e)}",
                "action_steps": [],
                "action_locations": [],
                "governing_bodies": [],
                "consulted_stakeholders": [],
                "rationale": "",
                "constraint_assessment": ""
            }
    
    def _get_evaluator_decision(self, evaluator_context: Dict[str, Any], trace_id: str, revision_cycle: int, dialog_memory: str) -> Dict[str, Any]:
        """Call the evaluator twin to assess the proposed_action."""
        
        event_start = time.time()

        try:
            # self._evaluator_twin = EvaluatorTwin()
            if self._evaluator_twin is None:
                self._evaluator_twin = EvaluatorTwin()

            token_usage = self._evaluator_twin.provider.get_token_usage()
            tokens_before = token_usage["output_tokens"]
            result = self._evaluator_twin.evaluate_response(evaluator_context, dialog_memory)
            token_usage = self._evaluator_twin.provider.get_token_usage()
            tokens_after = token_usage["output_tokens"]
            tokens_used = tokens_after - tokens_before
            
            duration = (time.time() - event_start) * 1000
            decision = result.get("decision", "VETO")

            self._log_event("evaluator_decision", duration, tokens_used, True, {
                "decision": decision,
                "revision_cycle": revision_cycle,
                "trace_id": trace_id,
                "mode": self.mode
            })

            return result  # expected to be a flat evaluator_response dict

        except Exception as e:
            duration = (time.time() - event_start) * 1000
            self._log_event("evaluator_decision", duration, 0, False, {
                "revision_cycle": revision_cycle,
                "trace_id": trace_id
            }, str(e))

            return {
                "decision": "VETO",
                "rationale": f"Evaluator twin error: {str(e)}",
                "risk_analysis": "",
                "regulatory_assessment": "",
                "clarification_request": {}
            }
    
    def _should_escalate(self, decision: str) -> bool:
        """Determine if response should be escalated to human review."""
        
        print(f"\n\n\n=====Safety Socket: The decision in _should_escalate\n{decision}")

        # Escalate if decision is VETO
        if decision == "VETO":
            return True
        
        # Escalate if we hit max revisions
        if decision == "REVISION":
            return True
        
        # Escalate if evaluator is uncertain (future: confidence scores)
        # For now, just log that we would escalate
        
        return False
    
    def _build_telemetry_summary(self, trace_id: str) -> Dict[str, Any]:
        """Build comprehensive telemetry summary."""
        
        events_for_trace = [e for e in self._telemetry_events 
                           if e.metadata.get("trace_id") == trace_id]
        
        return {
            "trace_id": trace_id,
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "mode": self.mode,
            "total_events": len(events_for_trace),
            "successful_events": sum(1 for e in events_for_trace if e.processed),
            "events": [asdict(event) for event in events_for_trace]
        }
            
    def _save_detailed_telemetry(self, response: SafetyResponse) -> None:
        """Save detailed telemetry using configured provider."""
        
        telemetry_data = {
            "response": {
                "processed": response.processed,
                "final_decision": response.final_decision,
                "revision_count": response.revision_count,
                "total_duration_ms": response.total_duration_ms,
                "session_id": response.session_id,
                "trace_id": response.trace_id,
                "reason": response.reason,
                "rationale": response.rationale
            },
            "telemetry": response.telemetry,
            "contract": response.contract,
            "metadata": {
                "config_mode": self.mode,
                "max_revision_cycles": self.max_revision_cycles,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        try:
            # Route to appropriate telemetry provider
            if self.telemetry_provider == "local_json":
                self._save_telemetry_json(telemetry_data, response.trace_id)
            elif self.telemetry_provider == "local_jsonl":
                self._save_telemetry_jsonl(telemetry_data, response.trace_id)
            elif self.telemetry_provider == "postgresql":
                self._save_telemetry_postgresql(telemetry_data, response.trace_id)
            elif self.telemetry_provider == "elasticsearch":
                self._save_telemetry_elasticsearch(telemetry_data, response.trace_id)
            else:
                raise ValueError(f"Unsupported telemetry provider: {self.telemetry_provider}")
            
            # Log successful telemetry save
            self._log_event("telemetry_saved", 0, 0, True, {
                "provider": self.telemetry_provider,
                "trace_id": response.trace_id
            })
            print(f"\n\n\n=====Safety Socket: Telemetry saved\n{telemetry_data}")
        except Exception as e:
            # Log telemetry save failure but don't crash
            self._log_event("telemetry_save_failed", 0, 0, False, {
                "provider": self.telemetry_provider,
                "trace_id": response.trace_id
            }, str(e))
    
    def _save_telemetry_json(self, telemetry_data: Dict[str, Any], trace_id: str) -> None:
        """Save telemetry as individual JSON files."""
        filename = f"safety_socket_telemetry_{trace_id}.json"
        filepath = self.telemetry_output_path / filename
        print(f"===== Safety_Socket: Telemetry path {self.telemetry_output_path} ")
        
        with open(filepath, 'w') as f:
            json.dump(telemetry_data, f, indent=2)
    
    def _save_telemetry_jsonl(self, telemetry_data: Dict[str, Any], trace_id: str) -> None:
        """Save telemetry as JSONL (one line per request)."""
        filename = "safety_socket_telemetry.jsonl"
        filepath = self.telemetry_output_path / filename
        print(f"===== Safety_Socket: Telemetry path {self.telemetry_output_path} ")
        
        with open(filepath, 'a') as f:
            json.dump(telemetry_data, f)
            f.write('\n')
    
    def _save_telemetry_postgresql(self, telemetry_data: Dict[str, Any], trace_id: str) -> None:
        """Save telemetry to PostgreSQL database (stub for future implementation)."""
        # TODO: Implement PostgreSQL telemetry storage
        # Will need: connection config, table schema, insertion logic
        raise NotImplementedError("PostgreSQL telemetry provider not yet implemented")
    
    def _save_telemetry_elasticsearch(self, telemetry_data: Dict[str, Any], trace_id: str) -> None:
        """Save telemetry to Elasticsearch (stub for future implementation)."""
        # TODO: Implement Elasticsearch telemetry storage  
        # Will need: ES client, index configuration, document insertion
        raise NotImplementedError("Elasticsearch telemetry provider not yet implemented")
        
    def _log_from_response(self, response: SafetyResponse, event_type: str):
        self._log_event(
            event_type,
            response.total_duration_ms,
            0,
            response.processed,
            {
                "trace_id": response.trace_id,
                "final_decision": response.final_decision,
                "prompt_processing": response.prompt_processing,
                "escalated": response.escalated,
                "revision_count": response.revision_count,
                "reason": response.reason,
                "rationale": response.rationale
            }
        )

    def _log_event(self, event_type: str, duration_ms: float, tokens_used: int, processed: bool,
                   metadata: Dict[str, Any], error_message: str = None) -> None:
        """Log telemetry event."""
        
        event = TelemetryEvent(
            timestamp=time.time(),
            event_type=event_type,
            duration_ms=duration_ms,
            output_tokens=tokens_used,
            processed=processed,
            metadata=metadata,
            error_message=error_message
        )
        
        self._telemetry_events.append(event)

    def categorize_response_for_ui(self, response: SafetyResponse) -> UIClassification:
        # TODO - this break out is not quite right
        if not response.processed:
            return "error"

        if response.prompt_processing == "INVALID":
            return "clarification"

        if response.prompt_processing == "REJECTED":
            return "policy_violation"

        if response.escalated:
            return "escalation"

        return "success"