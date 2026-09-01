import datetime
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Callable

from ai_invoice_to_json.exceptions import ExtractionEvalError
from ai_invoice_to_json.schema import Invoice


@dataclass
class FieldResult:
    field_name: str
    correct: bool
    expected: Any
    actual: Any
    ambiguous: bool = False


def normalize_string(s: str) -> str:
    return s.strip()


def compare_field(
    field_name: str,
    expected: Any,
    actual: Any,
    normalize: Callable[[Any], Any] | None = None,
) -> FieldResult:
    if expected is None and actual is None:
        return FieldResult(field_name, True, expected, actual)
    if expected is None or actual is None:
        return FieldResult(field_name, False, expected, actual)

    if isinstance(expected, str) and isinstance(actual, str):
        norm = normalize or normalize_string
        e, a = norm(expected), norm(actual)
        return FieldResult(field_name, e == a, e, a)

    if isinstance(expected, (Decimal, int, float)) and isinstance(
        actual, (Decimal, int, float)
    ):
        return FieldResult(
            field_name, Decimal(str(expected)) == Decimal(str(actual)), expected, actual
        )

    if isinstance(expected, datetime.date) and isinstance(actual, datetime.date):
        return FieldResult(field_name, expected == actual, expected, actual)

    raise ExtractionEvalError(
        f"Field {field_name}: unsupported or mismatched types. expected {type(expected)}, actual {type(actual)}"
    )


def compare_nested(
    prefix: str, expected_dict, actual_dict, ambiguous_fields
) -> list[FieldResult]:
    results: list[FieldResult] = []

    for k, v in expected_dict.items():
        field_name = k if not prefix else f"{prefix}.{k}"
        fr = compare_field(field_name, v, actual_dict.get(k))
        if k in ambiguous_fields:
            fr.ambiguous = True
        results.append(fr)

    return results


def compare_products(
    expected: list[dict], actual: list[dict], ambiguous_fields
) -> list[FieldResult]:
    product_fields = ["product_name", "quantity", "unit_price"]
    results: list[FieldResult] = []

    # lookup dicts
    expected_by_id = {p["product_id"]: p for p in expected}
    actual_by_id = {p["product_id"]: p for p in actual}

    for pid, exp_product in expected_by_id.items():
        prefix = f"products.{pid}"

        if pid not in actual_by_id:
            fr = FieldResult(
                f"{prefix}.<missing>", correct=False, expected=exp_product, actual=None
            )
            results.append(fr)
            continue

        act_product = actual_by_id[pid]
        for field in product_fields:
            field_name = f"{prefix}.{field}"
            fr = compare_field(
                field_name, exp_product.get(field), act_product.get(field)
            )
            if field_name in ambiguous_fields:
                fr.ambiguous = True
            results.append(fr)

    for pid, act_product in actual_by_id.items():
        if pid not in expected_by_id:
            fr = FieldResult(
                f"products.{pid}.<extra>",
                correct=False,
                expected=None,
                actual=act_product,
            )
            results.append(fr)

    return results


def score_invoice(predicted: Invoice, ground_truth: dict) -> list[FieldResult]:
    ambiguous_fields = set(ground_truth.get("_ambiguous_fields", {}).keys())
    predicted_dict = predicted.model_dump()
    results = []

    # top-level non-nested fields
    top_level_keys = [
        "currency",
        "order_id",
        "customer_id",
        "order_date",
        "total_price",
    ]
    for key in top_level_keys:
        fr: FieldResult = compare_field(
            key, ground_truth.get(key), predicted_dict.get(key)
        )
        if key in ambiguous_fields:
            fr.ambiguous = True
        results.append(fr)

    # compare nested fields
    results += compare_nested(
        "customer_details",
        ground_truth["customer_details"],
        predicted_dict["customer_details"],
        ambiguous_fields,
    )

    results += compare_products(
        ground_truth["products"],
        predicted_dict["products"],
        ambiguous_fields,
    )

    return results
