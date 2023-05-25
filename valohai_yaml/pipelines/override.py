from collections import OrderedDict
from typing import Any, List, Optional


def merge_overridden_inputs(overridden_inputs: List[OrderedDict], step_inputs: List[OrderedDict]) -> List[OrderedDict]:
    merged_inputs = []
    dict1_map = {overridden_input['name']: overridden_input for overridden_input in overridden_inputs}
    for step_input in step_inputs:
        name = step_input['name']
        if name in dict1_map:
            ordered_dict1 = dict1_map[name]
            merged_dict = OrderedDict()
            for key, value in ordered_dict1.items():
                if key == 'default':
                    merged_dict[key] = merge_defaults(value, step_input.get(key))
                else:
                    merged_dict[key] = value
            merged_inputs.append(merged_dict)
        else:
            merged_inputs.append(step_input)
    for ordered_dict1 in overridden_inputs:
        name = ordered_dict1['name']
        if name not in dict1_map:
            merged_inputs.append(ordered_dict1)
    return merged_inputs


def merge_defaults(default1: Optional[Any], default2: Optional[Any]) -> List[str]:
    default1 = [default1] if isinstance(default1, str) else (default1 if default1 else [])
    default2 = [default2] if isinstance(default2, str) else (default2 if default2 else [])
    return default1 + default2
