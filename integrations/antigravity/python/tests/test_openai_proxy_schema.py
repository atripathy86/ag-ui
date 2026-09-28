"""Schema repair in the example OpenAI shim (examples/server/openai_proxy.py)."""

import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "examples", "server")
)

from openai_proxy import _normalize_schema  # noqa: E402


def test_proto_style_type_names_are_lowercased_at_any_depth():
    schema = {
        "type": "OBJECT",
        "properties": {"items": {"type": "ARRAY", "items": {"type": "STRING"}}},
    }
    assert _normalize_schema(schema) == {
        "type": "object",
        "properties": {"items": {"type": "array", "items": {"type": "string"}}},
    }


def test_a_parameter_named_type_is_still_normalized():
    # Under `properties`, "type" is a field name whose value is a schema. It
    # used to be treated as a type keyword and skipped, so the field kept
    # "STRING" and OpenAI rejected the whole tool.
    schema = {"type": "OBJECT", "properties": {"type": {"type": "STRING"}}}
    assert _normalize_schema(schema) == {
        "type": "object",
        "properties": {"type": {"type": "string"}},
    }
