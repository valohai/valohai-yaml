import enum
import importlib
import inspect
import pkgutil

import valohai_yaml.objs
import valohai_yaml.objs.pipelines


def _collect_public_names(package):
    """Collect all public class/enum names defined in a package's submodules."""
    public_names = {}
    package_path = package.__path__
    package_prefix = package.__name__ + "."

    for _importer, modname, _ispkg in pkgutil.walk_packages(package_path, prefix=package_prefix):
        module = importlib.import_module(modname)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name.startswith("_"):
                continue
            # Only include classes actually defined in this module (not imported from elsewhere)
            if obj.__module__ != module.__name__:
                continue
            # Only include classes and enums, not e.g. TypeVars
            if not (isinstance(obj, type) and (issubclass(obj, (valohai_yaml.objs.Item, enum.Enum)) or name == "Item")):
                continue
            public_names[name] = module.__name__
    return public_names


def test_objs_reexports_all_public_classes():
    """All public classes/enums in valohai_yaml.objs submodules are re-exported from __init__."""
    defined = _collect_public_names(valohai_yaml.objs)
    exported = set(valohai_yaml.objs.__all__)
    missing = set(defined) - exported
    assert not missing, (
        f"The following classes are defined in valohai_yaml.objs submodules "
        f"but not listed in valohai_yaml.objs.__all__: "
        f"{', '.join(f'{name} (from {defined[name]})' for name in sorted(missing))}"
    )
    # Also verify they're actually importable from the package
    for name in exported:
        assert hasattr(valohai_yaml.objs, name), f"{name} is in __all__ but not importable from valohai_yaml.objs"


def test_pipelines_reexports_all_public_classes():
    """All public classes/enums in valohai_yaml.objs.pipelines submodules are re-exported from __init__."""
    defined = _collect_public_names(valohai_yaml.objs.pipelines)
    exported = set(valohai_yaml.objs.pipelines.__all__)
    missing = set(defined) - exported
    assert not missing, (
        f"The following classes are defined in valohai_yaml.objs.pipelines submodules "
        f"but not listed in valohai_yaml.objs.pipelines.__all__: "
        f"{', '.join(f'{name} (from {defined[name]})' for name in sorted(missing))}"
    )
    for name in exported:
        assert hasattr(valohai_yaml.objs.pipelines, name), (
            f"{name} is in __all__ but not importable from valohai_yaml.objs.pipelines"
        )
