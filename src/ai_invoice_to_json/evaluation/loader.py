import json
from pathlib import Path

from ai_invoice_to_json.schema import Invoice


def load_ground_truth(file_path: str | Path) -> dict:
    with open(file_path, encoding="utf-8") as f:
        raw = json.load(f)

    ambiguous_fields = raw.pop("_ambiguous_fields", {})

    # validate through Invoice itself
    invoice = Invoice(**raw)
    ground_truth_dict = invoice.model_dump()
    ground_truth_dict["_ambiguous_fields"] = ambiguous_fields

    return ground_truth_dict
