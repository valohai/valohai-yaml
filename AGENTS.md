# Guidance for coding agents

`valohai-yaml` parses, validates and lints `valohai.yaml` files.
It is a published library with downstream consumers, and it supports Python 3.9 and up.

## Commands

```bash
make dev                  # install the package, test dependencies and pre-commit hooks
make lint                 # pre-commit: ruff, ruff-format, mypy, prettier
make test                 # pytest
pytest --snapshot-update  # regenerate syrupy snapshots
```

Get `make lint` and `make test` green before finishing.

## Layout

- `valohai_yaml/schema_data.py`: the JSON schemas used for validation, as Python dicts.
  Schema keys are kebab-case, never underscored.
- `valohai_yaml/objs/`: the classes a config parses into, all subclasses of `Item`.
  `Item.parse` maps kebab-case YAML keys to snake_case keyword arguments, and `serialize` maps them back.
- `valohai_yaml/types.py`: TypedDicts for dict-shaped values.
- `examples/`: valid configs.
  Each one is validated through the CLI by the test suite.
- `tests/error_examples/`, `tests/warning_examples/`: configs that must fail validation or produce lint warnings.
  Their CLI output is snapshotted in `tests/__snapshots__/`.

## Adding or changing a YAML property

A property usually touches all of these:

1. The schema in `schema_data.py`.
2. The object class in `objs/`: a keyword-only `__init__` argument, plus `lint()` for checks the schema can't express.
3. An example in `examples/`, extended or new.
   Register a new file in `tests/conftest.py` with `config_fixture`,
   which runs each test both directly and through a serialize/parse round trip.
4. A test asserting the parsed value.
5. For a new validation error or lint warning, a file in `tests/error_examples/` or `tests/warning_examples/`,
   and updated snapshots.
   Read the snapshot diff before accepting it.

New public classes in `objs/` must be re-exported in the package's `__all__`.

Leave `CHANGELOG.md` and `__version__` alone; they change in release commits.

## Scope

- Do only what the task asks:
  no speculative options or abstractions, no drive-by fixes, and no reformatting of lines you aren't changing.
  Mention unrelated problems in your summary instead.
- Look for an existing helper, fixture or pattern before writing a new one.
- Delete what your change makes unused.
  No commented-out code or debug output.
- Existing configs must keep parsing and validating.
  Add properties alongside old ones;
  don't rename or remove properties, public names or serialized output unless that is the task.
- Don't add a dependency for something the standard library or an existing dependency does.

## Code

- Use absolute imports (relative imports are banned) and `from __future__ import annotations`.
  Check that syntax and stdlib APIs exist in Python 3.9.
- Flags and optional parameters are keyword-only.
  Prefer early returns to nesting.
- Types match reality: nothing optional that is never absent,
  and a TypedDict or enum rather than a loose `dict` or `str`.
- Don't silence ruff or mypy to get green; restructure.
  An unavoidable suppression is narrow and has a comment saying why.
- A YAML file is user input:
  report problems as validation errors or lint results with a message that names the offending item and value.
  Elsewhere, fail loudly rather than returning `None` or swallowing exceptions.
- `0`, `""` and `[]` are values; test for `None` explicitly.
- Comment only the non-obvious why.
  No docstrings that restate the name.

## Tests

- Write the fewest tests that prove the change, and extend an existing test of the same path before adding a new one.
- For a bug fix, confirm the test fails without the fix.
- Test through `parse`, `validate`, `lint` or the CLI, and assert the whole result rather than its length or truthiness.
- Parametrize cases that share setup and assertions.
- Change an existing assertion or snapshot only when the task changes that behaviour, and say so in your summary.

## Commits and pull requests

- One logical change per commit, with an imperative subject.
  Refactors and renames go in separate, earlier commits.
- One topic per pull request.
  Rebase on `master` rather than merging it in.
- The description says why the change exists, lists every behaviour change, and says how it was tested.
