# cbyb/utils/yaml_help.py
""" Yaml helpers """

def yaml_to_string(data, indent=0) -> str:
    """ Take a dict and make string .. used in prompt engineering """
    spacer = "  " * indent
    if isinstance(data, dict):
        return "\n".join(f"{spacer}{k.replace('_', ' ').title()}:\n{yaml_to_string(v, indent + 1)}"
                         for k, v in data.items())
    elif isinstance(data, list):
        return "\n".join(f"{spacer}- {yaml_to_string(v, indent + 1) if isinstance(v, (dict, list)) else v}"
                         for v in data)
    else:
        return f"{spacer}{data}"