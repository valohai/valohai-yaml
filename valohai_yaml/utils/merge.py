import copy
from typing import Any, Callable, List, MutableMapping, TypeVar

MISSING = object()

TMerge = TypeVar("TMerge")
TCopy = TypeVar("TCopy")
TD = TypeVar("TD", bound=MutableMapping[Any, Any])


def merge_dicts(
    a: TD,
    b: TD,
    merger: Callable[[TMerge, TMerge], TMerge],
    copier: Callable[[TCopy], TCopy] = lambda v: v,
    skip_missing_a: bool = False,
    skip_missing_b: bool = False,
) -> TD:
    out: TD = type(a)()

    # Hack to keep the iteration order the same...
    keys: List[Any] = list(a)
    key_set = set(keys)
    keys += [k for k in b if k not in key_set]

    for key in keys:
        va = a.get(key, MISSING)
        vb = b.get(key, MISSING)
        if vb is MISSING:
            if not skip_missing_b:
                out[key] = copier(va)
        elif va is MISSING:
            if not skip_missing_a:
                out[key] = copier(vb)
        else:
            out[key] = merger(va, vb)
    return out


def merge_simple(a: TMerge, b: TMerge) -> TMerge:
    a = copy.deepcopy(a)
    a.__dict__.update(copy.deepcopy(b).__dict__)
    return a
