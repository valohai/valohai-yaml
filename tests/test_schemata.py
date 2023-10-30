from pathlib import Path

from valohai_yaml.validation import SCHEMATA_DIRECTORY


def test_schemata_has_no_underscores():
    for yaml_path in Path(SCHEMATA_DIRECTORY).rglob("*.yaml"):
        with yaml_path.open("r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                clean_line = line.partition("#")[0].strip()
                if clean_line.endswith(":") and "_" in clean_line:
                    raise AssertionError(
                        f"Underscore in YAML key in {yaml_path!r}:{lineno}: {line!r}",
                    )
