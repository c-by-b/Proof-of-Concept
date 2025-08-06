# utils/json_utils.py
""" sundry helpers for working with JSON from LLMs """

import json
import re

def extract_dict_from_llm_response_original(response: str):
    """
    Extract and parse the first valid JSON object from an LLM response.
    Handles Markdown code fences and extraneous text.
    """
    # Remove markdown code fences like ```json ... ```
    code_block_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", response, re.DOTALL)
    if code_block_match:
        json_text = code_block_match.group(1)
    else:
        # Fallback: naive bracket extraction
        json_start = response.find('{')
        json_end = response.rfind('}') + 1

        if json_start == -1 or json_end == -1:
            raise json.JSONDecodeError("No JSON found in response", response, 0)

        json_text = response[json_start:json_end]

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Failed to parse JSON: {e}", json_text, e.pos)
    
def extract_dict_from_llm_response_old_old(response: str):
    """
    Extract and parse the first valid JSON object from an LLM response.
    Handles Markdown code fences and extraneous text.
    """
    # Match code-fenced JSON block (most robust first)
    code_block_match = re.search(r"```(?:json)?\s*({.*?})\s*```", response, re.DOTALL)
    if code_block_match:
        json_text = code_block_match.group(1)
    else:
        # Fallback: naive first-brace to last-brace extraction
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        if json_start == -1 or json_end == -1:
            raise json.JSONDecodeError("No JSON found in response", response, 0)
        json_text = response[json_start:json_end]

    # Optional: Strip control characters
    json_text = re.sub(r'[\x00-\x1F\x7F]', '', json_text)

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON from LLM response.")
        print("Raw candidate JSON:\n", json_text)
        raise json.JSONDecodeError(f"Failed to parse JSON: {e}", json_text, e.pos)
    
def extract_dict_from_llm_response_new(response: str):
    """
    Extract and parse the first valid JSON object from an LLM response.
    Handles optional markdown fences and fallbacks to raw JSON.
    """
    # Prefer markdown-wrapped JSON
    code_match = re.search(r"```json\s*({[\s\S]*})\s*```", response)
    if code_match:
        json_text = code_match.group(1)
    else:
        # Fallback: greedy brace-to-brace match
        json_match = re.search(r"({[\s\S]*})", response)
        if not json_match:
            raise json.JSONDecodeError("No JSON object found", response, 0)
        json_text = json_match.group(1)

    # Clean up weird control characters
    json_text = re.sub(r'[\x00-\x1F\x7F]', '', json_text)

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:")
        print("---- Raw extracted text ----")
        print(json_text)
        print("---- End of text ----")
        raise json.JSONDecodeError(f"Failed to parse JSON: {e}", json_text, e.pos)
    
def extract_dict_from_llm_response(response: str):
    """
    Extract and parse the first valid JSON object from an LLM response.
    Handles Markdown code fences, control characters, and fallback bracket extraction.
    """
    def clean_json_text(text):
        # Remove any control characters that aren't standard whitespace
        text = re.sub(r"[\x00-\x1f\x7f]", "", text)
        # Replace smart quotes and unicode dashes with standard equivalents
        text = text.replace("“", '"').replace("”", '"').replace("’", "'").replace("–", "-")
        return text.strip()

    # Try to extract code block first
    code_block_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", response, re.DOTALL)
    if code_block_match:
        json_text = code_block_match.group(1)
    else:
        # Fallback: bracket matching from first '{' to last '}'
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        if json_start == -1 or json_end == -1 or json_end <= json_start:
            raise json.JSONDecodeError("No JSON object found in response", response, 0)
        json_text = response[json_start:json_end]

    # Clean up the JSON text before parsing
    json_text = clean_json_text(json_text)

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Failed to parse JSON (likely bad escape or control char near pos {e.pos}): {e.msg}",
            json_text,
            e.pos
        )