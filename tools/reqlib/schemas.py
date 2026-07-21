"""Strict-schema validation for authored YAML layers (process.md §1 P2). Unknown keys are errors — the arkhive lesson that
strict schemas plus declared scalar types neutralize YAML implicit typing."""
import json
from pathlib import Path

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None

SCHEMA_DIR = Path(__file__).resolve().parent.parent.parent / "schema"

# authored-file → schema mapping; profiles/_index.yaml is presentation config
LAYER_SCHEMAS = {
    "prd": "prd.schema.json",
    "brd": "brd.schema.json",
    "profiles": "profiles.schema.json",
    "trace": "links.schema.json",
}


def _load(name, _cache={}):
    if name not in _cache:
        _cache[name] = _inline_refs(json.loads((SCHEMA_DIR / name).read_text()))
    return _cache[name]


def _inline_refs(node):
    """Resolve {"$ref": "<file>.schema.json"} by inlining the file — one
    hop is all keel's schemas use, so no resolver machinery."""
    if isinstance(node, dict):
        ref = node.get("$ref", "")
        if isinstance(ref, str) and ref.endswith(".schema.json"):
            return _load(ref)
        return {k: _inline_refs(v) for k, v in node.items()}
    if isinstance(node, list):
        return [_inline_refs(v) for v in node]
    return node


def schema_for(path):
    """Return the schema filename for an authored YAML path, or None."""
    if path.name.startswith("_"):
        return None
    return LAYER_SCHEMAS.get(path.parent.name)


def validate(path, data):
    """Return a list of 'file: message' error strings (empty = valid)."""
    name = schema_for(path)
    if name is None:
        return []
    if jsonschema is None:
        return [f"{path.name}: jsonschema not installed (pip install jsonschema)"]
    v = jsonschema.Draft7Validator(_load(name))
    out = []
    for e in sorted(v.iter_errors(data), key=lambda e: list(e.absolute_path)):
        loc = "/".join(str(p) for p in e.absolute_path) or "<root>"
        out.append(f"{path.name}: {loc}: {e.message}")
    return out
