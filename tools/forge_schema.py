#!/usr/bin/env python3
"""forge_schema.py — Minimal JSON Schema (draft-07 subset) validator, stdlib only.

Covers exactly the keywords FORGE's own schemas use: type (incl. unions),
required, properties, additionalProperties: false, enum, const, pattern,
minimum, maximum, minLength, minItems, maxItems, items, format (date,
date-time). Anything else is ignored. Use `check-jsonschema` for full
validation; this exists so the tools work with no `pip install`.

Usage:
    python forge_schema.py SCHEMA.json DATA.jsonl
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

_TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "null": type(None),
}


def _is_type(value, name: str) -> bool:
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    expected = _TYPES.get(name)
    return expected is not None and isinstance(value, expected)


def _format_ok(value: str, fmt: str) -> bool:
    try:
        if fmt == "date":
            date.fromisoformat(value)
        elif fmt == "date-time":
            if "T" not in value:
                return False
            datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def validate(value, schema: dict, path: str = "$") -> list:
    """Return a list of human-readable errors; empty means valid."""
    errors = []
    types = schema.get("type")
    if types is not None:
        names = types if isinstance(types, list) else [types]
        if not any(_is_type(value, n) for n in names):
            return [f"{path}: expected {'/'.join(names)}, got {type(value).__name__}"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} not in {schema['enum']}")
    if isinstance(value, str):
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: {value!r} does not match {schema['pattern']}")
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: shorter than {schema['minLength']}")
        if "format" in schema and not _format_ok(value, schema["format"]):
            errors.append(f"{path}: not a valid {schema['format']}")
    if _is_type(value, "number"):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: above maximum {schema['maximum']}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: fewer than {schema['minItems']} items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: more than {schema['maxItems']} items")
        if isinstance(schema.get("items"), dict):
            for i, item in enumerate(value):
                errors += validate(item, schema["items"], f"{path}[{i}]")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required field {key!r}")
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in props:
                    errors.append(f"{path}: unexpected field {key!r}")
        for key, sub in props.items():
            if key in value:
                errors += validate(value[key], sub, f"{path}.{key}")
    return errors


def load_schema(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_jsonl(schema: dict, data: Path) -> list:
    """Validate every non-empty line; return (line_number, error) pairs."""
    problems = []
    with Path(data).open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                problems.append((number, f"invalid JSON: {exc}"))
                continue
            problems += [(number, error) for error in validate(record, schema)]
    return problems


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2:
        print(__doc__.strip().splitlines()[-1].strip(), file=sys.stderr)
        return 2
    problems = validate_jsonl(load_schema(Path(argv[0])), Path(argv[1]))
    for number, error in problems:
        print(f"line {number}: {error}")
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
