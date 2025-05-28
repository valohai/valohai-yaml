"""One-shot script to convert the YAML schema files shipped in valohai_yaml/schema/ into a Python module."""

import pathlib
from io import StringIO
from pprint import pformat

import yaml

PRELUDE = """
SCHEMATA = {}
def register(schema: dict) -> None:
    SCHEMATA[schema["$id"]] = schema
"""
POSTLUDE = """
del register
"""


def fixup_refs(data: dict) -> None:
    if isinstance(data, dict):
        if ref := (data.get("$ref")):
            assert len(data) == 1
            if ref.startswith("./"):
                stem = ref[2:].removesuffix(".json")
                ref = f"/schemas/{stem}"
            else:
                raise NotImplementedError(f"???: {ref}")
            data["$ref"] = ref
        else:
            for _key, value in data.items():
                fixup_refs(value)
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                fixup_refs(item)


def main() -> None:
    out_fp = StringIO()
    out_fp.write(PRELUDE)

    for f in sorted(
        pathlib.Path("./valohai_yaml/schema").glob("*.yaml"),
        key=lambda x: x.stem,
    ):
        id = f"https://valohai.com/schemas/{f.stem}"
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        data["$id"] = id
        fixup_refs(data)
        out_fp.write(f"register({pformat(data, width=120)},)\n")
    out_fp.write(POSTLUDE)

    with open("./valohai_yaml/schema_data.py", "w", encoding="utf-8") as out_file:
        out_file.write(out_fp.getvalue())


if __name__ == "__main__":
    main()
