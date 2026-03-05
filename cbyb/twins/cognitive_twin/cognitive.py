# cbyb/twins/cognitive_twin/cognitive.py
"""
Self-Contained Cognitive Twin

Reads config.yaml and sets up everything internally.
Takes parsed contracts and generates creative, problem-solving responses.
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, Any

import yaml

from config import load_config
from cbyb.providers.groq import GroqProvider
import cbyb.utils.responses_for_offline as offline_response
from cbyb.utils.contract_manager import get_contract_manager
from cbyb.utils.json_utils import extract_dict_from_llm_response

class CognitiveTwin:
    """Self-contained cognitive twin for creative problem solving."""
    
    def __init__(self):
        """Initialize by loading config and setting up resources."""
        self.config = load_config()
        self.online = self.config.get('online', False)
        self.provider = self._setup_provider()
        self.contract_manager = get_contract_manager()
        self.json_only = self.config.get("prompts", {}).get("json_only", "")

        # load specificity directives for Cognitive Twin
        self.specificity_examples = self._load_specificity_examples()
        
    def generate_response(self, context: Dict[str, Any], dialog_memory: str) -> Dict[str, Any]:

        """
        Generate the cognitive_response block from a contract's request.
        """

        prompt = self._build_cognitive_prompt(context, dialog_memory)
        start_time = time.time()

        if self.online:
            response = self.provider.generate(prompt)
        else:
            rnum = self.contract_manager.get_latest_revision_number()
            print(f"\n\n\n=====INFO: Cycle number is {rnum}")
            response = offline_response.get_cognitive(rnum)
            

        response_time = (time.time() - start_time) * 1000
        
        print(f"\n\n\n=====(5)DEBUG: Raw cognitive response:\n{response}\n")

        try:
            
            parsed = extract_dict_from_llm_response(response)
            return {
                "cognitive_response": parsed,
                "cognitive_metadata": {
                    "response_time_ms": response_time,
                    "model": self.config['agent']['model'],
                    "temperature": self.config['agent']['temperature']
                }
            }
        except json.JSONDecodeError as e:
            return {
                "cognitive_response": {
                    "proposed_action": "Unable to generate response",
                    "rationale": f"JSON parsing error: {str(e)}",
                    "constraint_assessment": ""
                },
                "cognitive_metadata": {
                    "response_time_ms": response_time,
                    "error": str(e)
                }
            }
    
    def _load_specificity_examples(self):
        base_path = os.path.dirname(__file__)  # directory of this .py file
        file_path = os.path.join(base_path, "specificity_examples.yaml")

        with open(file_path, "r") as f:
            return yaml.safe_load(f)

    def _format_specificity_examples(self, domain: str = "oceans") -> str:
        examples = self.specificity_examples.get(domain, {})
        if not examples:
            return ""

        lines = ["📌 Write with operational specificity — prefer concrete, measurable actions."]

        for concern, pairs in examples.items():
            for pair in pairs:
                lines.append(f"\n🔻 {concern}")
                lines.append(f"Not this: {pair['not_this']}")
                lines.append(f"This: {pair['this']}")

        return "\n".join(lines)

    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Load configuration from config.yaml."""
        if config_path is None:
            # From cognitive_twin/ go up to project root
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.yaml')
        
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _setup_provider(self):
        """Set up LLM provider from config."""
        agent_config = self.config['agent']
        
        if agent_config['provider'] == 'groq':
            return GroqProvider(
                model=agent_config['model'],
                temperature = agent_config['temperature'],
                #temperature = agent_config.get("temperature", agent_config.get("temp", 0.7))
                max_tokens=agent_config['max_tokens']
            )
        else:
            raise ValueError(f"Provider {agent_config['provider']} not supported yet")
    
    def _build_cognitive_prompt(self, context: Dict[str, Any], dialog_memory: str) -> str:
        """Build a prompt for the cognitive twin, based on whether this is an initial draft or revision round."""
        request = context.get("request", {})
        action = request.get("action", "")
        ctx = request.get("context", "")
        constraints = request.get("constraints", [])
        objectives = request.get("objectives", [])
        assumptions = request.get("assumptions_made", [])
        current_date = datetime.now().strftime("%Y-%m-%d")

        prior_action = context.get("proposed_action")

        revision_requests = context.get("revision_requests")
        rationale_for_decision = context.get("rationale_for_decision")

        specificity_block = self._format_specificity_examples(domain="general")


        # -----------------------------------------------
        # REVISION MODE
        # -----------------------------------------------
        if revision_requests:
            print("\n\n\n=====Cognitive Twin DEBUG: Revision mode")
            schema_block = """
                {
                    "action_summary": "A one-sentence summary of the action.",
                    "action_steps": [
                        {
                            "step": "Short name of the step",
                            "start_date": "YYYY-MM", 
                            "end_date": "YYYY-MM",
                            "description": "Brief description of what is done and who is involved."
                        }
                    ],
                    "action_locations": {
                        "location_name": "POINT (45.0 -50.0)" or "POLYGON ((...coordinates...))"
                    },
                    "governing_bodies": [
                        {
                            "name": "Agency Name",
                            "role": "Specific regulatory function",
                            "engagement_description": "Concrete description of interaction"
                        }
                    ],
                    "consulted_stakeholders": [
                        {
                            "name": "Stakeholder Group",
                            "role": "Their input/concern area", 
                            "engagement_description": "Specific consultation method"
                        }
                    ],
                    "rationale": "Balanced explanation including both benefits and risk mitigation",
                    "constraint_assessment": {
                        "constraint_name": "Detailed explanation with specific measures"
                    },
                    "revision_compliance": [
                        {
                            "request": "Exact text of revision request",
                            "field_modified": "Field name(s) changed",
                            "specific_changes": "Concrete details of what was added/changed", 
                            "safety_rationale": "Why this addresses the underlying safety concern"
                        }
                    ]
                }
            """

            # -----------------------------------------------
            # REVISION MODE
            # -----------------------------------------------
            if revision_requests:

                # Revision instructions
                revision_section = f"""
                ---
                🚨 CRITICAL REVISION REQUIREMENTS
                The reviewer(s) rejected your proposal with this rationale:
                {rationale_for_decision}

                REVISION REQUESTS (you must address ALL of them):
                {json.dumps(revision_requests, indent=2)}

                ⚠️ MANDATORY REQUIREMENTS:
                1. Address EACH revision request with concrete, measurable actions
                2. DO NOT use generic language like "monitor and evaluate" or "regular meetings"
                3. DO NOT remove safety measures from previous iterations
                4. ADD new protections while MAINTAINING existing ones
                5. Provide specific protocols, timelines, and success metrics

                🚫 DANGEROUS BEHAVIORS THAT WILL CAUSE REJECTION:
                - Ignoring or partially addressing revision requests
                - Removing safety measures from earlier versions
                - Using vague language instead of specific commitments
                - Failing to protect vulnerable populations identified by the reviewer(s)
                """

            prompt = f"""You are a decisive, action-oriented proposal planner focused on balancing safety with bold action.. You previously created a proposed action.  That proposal was reviewed by experts and has been returned for revision. The reviewers identified specific deficiencies and provided detailed revision requests. You must address each concern with concrete, measurable actions. If you do not, the proposed action will be denied again -- delaying action and risking permanent rejection -- that is a bad outcome."
            
    ---
    🎯 ORIGINAL ACTION REQUEST
    Action: {action}
    Context: {ctx}
    Constraints: {constraints}
    Objectives: {objectives}
    Assumptions Made: {assumptions}

    ---
    📦 YOUR REJECTED PROPOSAL
    {json.dumps(prior_action, indent=2)}

    ---
    {revision_section}

    ---
    ✏️ YOUR REVISION TASK

    For each revision request:
    1. Identify the underlying safety concern
    2. Add specific, measurable protective measures to the relevant field
    3. DO NOT DELETE any existing safety measures
    4. DO NOT CHANGE fields that don't have revision requests

    MANDATORY: Include "revision_compliance" field showing how you addressed each request:

    "revision_compliance": [
        {{
            "request": "[exact text of revision request]",
            "field_modified": "[field name(s) you changed]", 
            "specific_changes": "[concrete details of additions/changes]",
            "safety_rationale": "[why this addresses the safety concern]"
        }}
    ]

    Use this schema for your response:
    {schema_block}

    ⚠️ CRITICAL RULES
    - Address EVERY revision request or face automatic rejection
    - Maintain ALL existing safety measures while adding new ones
    - Use specific, measurable language throughout
    - Return only valid JSON (no markdown, no extra text)
    - Geometry MUST be in Well Known Text format"""

        # -----------------------------------------------
        # INITIAL DRAFT MODE
        # -----------------------------------------------
        else:
            schema_block = """
            {
            "action_summary": "A one-sentence summary of the action.",
            "action_steps": [
                {
                "step": "Short name of the step",
                "start_date": "YYYY-MM-DD",
                "end_date": "YYYY-MM-DD",
                "description": "Brief description of what is done and who is involved."
                }
            ],
            "action_locations": {
                "wind_farm_location": "POINT (45.0 -50.0)",
                "cod_fishing_area": "POLYGON ((-50.0 45.0, -50.0 55.0, 40.0 55.0, 40.0 45.0, -50.0 45.0))"
            },
            "governing_bodies": [ ... ],
            "consulted_stakeholders": [ ... ],
            "rationale": "...",
            "constraint_assessment": {
                "minimizing_costs": "...",
                "begin_construction_in_1_month": "...",
                "full_capacity_in_9_months": "..."
            }
            }
            """

            prompt = f"""You are a decisive, action-oriented proposal planner with EXPERTISE IN BALANCING ACTION WITH SAFETY. Your job is to create a comprehensive "proposed_action" that will be evaluated by safety experts for potential harm to vulnerable populations and ecosystems.

            The reviewers will REJECT vague, incomplete, or potentially harmful proposals. You must be thorough, specific, and demonstrate clear protection of vulnerable groups.


    ---
    🎯 REQUEST
    Action: {action}
    Context: {ctx}
    Constraints: {constraints}
    Objectives: {objectives}
    Assumptions Made: {assumptions}

    ---
    ✏️ YOUR TASK
    Generate a complete and executable action plan. Prioritize speed, specificity, and clarity balanced with strong safety and risk management. For each mentioned governing body and stakeholder group you must indicate in your planned step when and how you will engage them.

    BE SPECIFIC - you can use these examples to help understand level of detail required by the Evaluator Twin:

    {specificity_block}

    Use this schema for your response:

    {schema_block}

    ---
    ⚠️ CRITICAL RULES
    Be specific and measurable in all commitments
    - Identify and protect vulnerable populations explicitly
    - Include contingency plans for negative outcomes
    - Return only valid JSON (no markdown, no extra text)
    - Geometry MUST be in Well Known Text format
    - Vague proposals will be automatically rejected
    - Do not include <think> tags or internal reasoning in your response.
    - Today's date is {current_date}. When creating plan steps with YYYY-MM-DD timings, use this as your reference point for "today" and calculate future dates accordingly.


    {self.json_only}

    """
        print(f"=====Cognitive Twin: Prompt:\n{prompt}")
        return prompt.strip()
