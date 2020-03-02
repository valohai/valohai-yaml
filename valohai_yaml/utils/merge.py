import copy

from valohai_yaml.objs import Step, Config

MISSING = object()


def _merge_dicts(a: dict, b: dict, merger, copier=lambda v: v) -> dict:
    out = {}

    # Hack to keep the iteration order the same...
    keys = list(a)
    key_set = set(keys)
    keys += [k for k in b if k not in key_set]

    for key in keys:
        va = a.get(key, MISSING)
        vb = b.get(key, MISSING)
        if vb is MISSING:
            out[key] = copier(va)
        elif va is MISSING:
            out[key] = copier(vb)
        else:
            out[key] = merger(va, vb)
    return out


def _merge_simple(a, b):
    a = copy.deepcopy(a)
    a.__dict__.update(copy.deepcopy(b).__dict__)
    return a


def _merge_config(a: Config, b: Config) -> Config:
    result = Config()
    result.steps.update(_merge_dicts(a.steps, b.steps, _merge_step))
    return result


def _merge_step(a: Step, b: Step) -> Step:
    # If user first types "learning_rage", creates config, and finally fixes the typo,
    # they don't want to end up with both "learning_rage" and "learning_rate" after the merge.
    # So only merge parameters and inputs that are part of both configs (a & b).
    cleaned_parameters_a = {key: a.parameters[key] for key in a.parameters if key in b.parameters.keys()}
    cleaned_inputs_a = {key: a.inputs[key] for key in a.inputs if key in b.inputs.keys()}

    parameters = _merge_dicts(
        cleaned_parameters_a, b.parameters, merger=_merge_simple, copier=copy.deepcopy,
    )
    inputs = _merge_dicts(
        cleaned_inputs_a, b.inputs, merger=_merge_simple, copier=copy.deepcopy,
    )
    # TODO: Logic for merging with existing command
    result = Step(name=b.name, image=b.image, command=b.command)
    result.parameters.update(parameters)
    result.inputs.update(inputs)
    return result
