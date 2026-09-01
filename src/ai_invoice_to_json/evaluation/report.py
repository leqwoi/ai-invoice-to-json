from dataclasses import dataclass

from ai_invoice_to_json.evaluation.scorer import FieldResult


@dataclass
class ReportSummary:
    document_id: str
    total_fields: int
    correct_count: int
    incorrect_count: int
    ambiguous_count: int
    strict_accuracy: float  # excludes ambiguous fields


def summarize(results: list[FieldResult], document_id: str) -> ReportSummary:
    strict_results = [r for r in results if not r.ambiguous]
    ambiguous_results = [r for r in results if r.ambiguous]

    correct_count = sum(r.correct for r in strict_results)
    total_strict = len(strict_results)
    strict_accuracy = (correct_count / total_strict) if total_strict else 0.0

    return ReportSummary(
        document_id=document_id,
        total_fields=len(results),
        correct_count=correct_count,
        incorrect_count=total_strict - correct_count,
        ambiguous_count=len(ambiguous_results),
        strict_accuracy=strict_accuracy,
    )


def print_report(results: list[FieldResult], document_id: str) -> None:
    summary = summarize(results, document_id)

    print("\n" + "=" * 60)
    print(f"  EVALUATION REPORT — {document_id}")
    print("=" * 60)

    print(
        f"\nStrict accuracy: {summary.strict_accuracy:.1%} "
        f"({summary.correct_count}/{summary.correct_count + summary.incorrect_count} fields, "
        f"ambiguous fields excluded)"
    )
    if summary.ambiguous_count:
        print(f"Ambiguous fields (excluded from accuracy): {summary.ambiguous_count}")

    incorrect = [r for r in results if not r.correct and not r.ambiguous]
    if incorrect:
        print(f"\n--- INCORRECT FIELDS ({len(incorrect)}) ---")
        for r in incorrect:
            print(f"  ✗ {r.field_name}")
            print(f"      expected: {r.expected!r}")
            print(f"      actual:   {r.actual!r}")
    else:
        print("\n✓ No incorrect (non-ambiguous) fields.")

    ambiguous = [r for r in results if r.ambiguous]
    if ambiguous:
        print(f"\n--- AMBIGUOUS FIELDS ({len(ambiguous)}) — informational only ---")
        for r in ambiguous:
            status = "matched primary" if r.correct else "differed from primary"
            print(f"  ~ {r.field_name} ({status})")
            print(f"      expected: {r.expected!r}")
            print(f"      actual:   {r.actual!r}")

    correct = [r for r in results if r.correct and not r.ambiguous]
    print(f"\n--- CORRECT FIELDS ({len(correct)}) ---")
    for r in correct:
        print(f"  ✓ {r.field_name}")

    print("\n" + "=" * 60 + "\n")
