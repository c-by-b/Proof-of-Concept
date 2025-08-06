# cbyb/utils/contract_manager.py

import copy

class ContractManager:
    """ Manage the structure and updates to the contract used by Evaluator and Cognitive Twins """
    def __init__(self, contract=None):
        self.contract = contract if contract is not None else self.create_full_contract()


    # ----------------------------------------------------------------------
    # Contract Creation
    # ----------------------------------------------------------------------
    @staticmethod
    def create_full_contract():
        return {
            "prompt": "",
            "request": {
                "request_status": "",
                "action": "",
                "context": "",
                "constraints": [],
                "objectives": [],
                "assumptions_made": [],
                "request_metadata": {
                    "missing_info": [],
                    "is_valid": False
                }
            },
            "proposed_action": {
                "action_summary": "",
                "action_steps": [],
                "action_locations": [],
                "governing_bodies": [],
                "consulted_stakeholders": [],
                "rationale": "",
                "constraint_assessment": "",
                "revision_compliance": []
            },
            "paradata": {
                "revision_count": 0,
            },
            "dialog": {}  # revision history: { "r0": { "cognitive_response": {}, "evaluator_response": {} }, ... } 
        }

    # ----------------------------------------------------------------------
    # Contract Update Methods
    # ----------------------------------------------------------------------

    def update_revision_count(self):
        """At start of each revision, increment revision count by 1 (flat structure)."""
        try:
            paradata = self.contract["paradata"]
            paradata["revision_count"] = paradata["revision_count"] + 1
            updated_count = paradata["revision_count"]
            print(f"Revision count updated to {updated_count}")
            return updated_count

        except Exception as e:
            print(f"Exception in update_revision_count: {e}")
            raise

    def update_prompt(self, prompt: str):
        """Update contract.prompt from safety socket getting user prompt."""
        self.contract["prompt"] = prompt

    def update_request(self, parsed_request: dict):
        """Update contract.request from evaluator parsing of the user prompt."""
        self.contract["request"].update(parsed_request)

    def update_proposed_action(self, proposed_action: dict):
        """Update contract.proposed_action with the latest cognitive twin output."""
        self.contract["proposed_action"].update(proposed_action)

    def start_new_revision(self, new_rev_number):
        """Initialize a new dialog revision (rN)."""
        new_rev = f"r{new_rev_number}"
        self.contract["dialog"][new_rev] = {
            "cognitive_response": {},
            "evaluator_response": {}
        }
        print(f"New revision started using revision number {new_rev}")
        return new_rev_number

    def record_veto_response(self, veto_response: dict):
        """Update contract.veto_response with the evaluator response."""
        if "veto_response" not in self.contract or not isinstance(self.contract["veto_response"], dict):
            self.contract["veto_response"] = {}

        self.contract["veto_response"].update(veto_response)
        print(f"=====Contract Manager: veto_response updated:\n{self.contract['veto_response']}")

    def record_cognitive_response(self, cognitive_response: dict):
        """Store cognitive twin output in the latest dialog revision."""
        rev_key = f"r{self.get_latest_revision_number()}"
        self.contract["dialog"][rev_key]["cognitive_response"] = copy.deepcopy(cognitive_response)

        # Known structured fields
        allowed_fields = {
            "action_summary", "action_steps", "action_locations",
            "governing_bodies", "consulted_stakeholders",
            "rationale", "constraint_assessment", "revision_compliance"
        }

        # Separate core proposal and additional context
        structured = {}

        for key, val in cognitive_response.items():
            if key in allowed_fields:
                structured[key] = val
            else:
                pass

        # Update proposed_action with known structured fields
        self.update_proposed_action(structured)

        print("Cognitive response recorded")

    def record_evaluator_response(self, evaluator_response: dict):
        """Store evaluator twin output in the latest dialog revision."""
        rev_key = f"r{self.get_latest_revision_number()}"
        self.contract["dialog"][rev_key]["evaluator_response"] = copy.deepcopy(evaluator_response)
        print("\n\n\nEvaluator response recorded")

    def record_dialog_memory(self, dialog_memory: str):
        """Store a point in time summary of the dialog between twins."""
        self.contract["dialog"]["dialog_summary"] = copy.deepcopy(dialog_memory)
        print("\n\n\nDialog summary updated")

    def reset_contract(self):
        """Reset the entire contract structure."""
        self.contract = self.create_full_contract()

    # ----------------------------------------------------------------------
    # Accessors
    # ----------------------------------------------------------------------
    def get_request_for_evaluator(self) -> dict:
        """Return the request section for the evaluator to fill in from the user prompt."""
        request = copy.deepcopy(self.contract["request"])
        request.pop('request_metadata')
        return request

    def get_evaluator_context(self) -> dict:
        """Return the context that evaluator needs: request + current proposed_action."""
        request = copy.deepcopy(self.contract.get("request", {}))
        request.pop('request_status')
        return {
            "request": request,
            "proposed_action": copy.deepcopy(self.contract["proposed_action"])
        }
    
    def get_cognitive_context(self) -> dict:
        """Return the context the Cognitive Twin needs to revise its proposed_action."""
        request = copy.deepcopy(self.contract.get("request", {}))
        request.pop('request_status')
        context = {
            "request": request,
            "proposed_action": copy.deepcopy(self.contract.get("proposed_action", {})),
            "revision_requests": [],
            "rationale_for_decision": "",
            "revision": ""
        }

        dialog = self.contract.get("dialog", {})
        round_keys = [k for k in dialog if k.startswith("r") and k[1:].isdigit()]
        sorted_keys = sorted(round_keys, key=lambda k: int(k[1:]))

        # Find the most recent round that contains an evaluator_response with revision_requests
        last_revision_requests = []
        last_rationale = ""
        latest_key = ""

        for rev_key in reversed(sorted_keys):
            eval_resp = dialog.get(rev_key, {}).get("evaluator_response", {})
            if eval_resp.get("revision_requests"):
                last_revision_requests = eval_resp["revision_requests"]
                last_rationale = eval_resp.get("rationale_for_decision", "")
                latest_key = rev_key
                break

        # Inject into context for Cognitive Twin
        context["revision_requests"] = copy.deepcopy(last_revision_requests)
        context["rationale_for_decision"] = copy.deepcopy(last_rationale)
        context["revision"] = latest_key
        return context

    def get_dialog(self) -> dict:
        """Return the full dialog."""
        return copy.deepcopy(self.contract["dialog"])

    def get_latest_dialog_turn(self) -> dict:
        """Return the latest dialog round (cognitive + evaluator responses)."""
        rev_key = f"r{self.get_latest_revision_number()}"
        return copy.deepcopy(self.contract["dialog"].get(rev_key, {}))

    def get_latest_revision_number(self) -> int:
        """Return the current revision number."""
        count = self.contract["paradata"]["revision_count"]
        print(f"Latest revision number is {count}")
        return count
    
    def get_previous_revision_number(self) -> int:
        """Return the previous revision number"""
        count = self.contract.get("paradata", {}).get("revision_count", 0)
        return count - 1
    
    def get_final_contract(self) -> dict:
        return self.contract

# Create single shared instance
# TODO - get rid of this singleton and pass a contract manager as needed
_manager_instance = ContractManager()

def get_contract_manager():
    """Returns the shared contract manager instance"""
    return _manager_instance