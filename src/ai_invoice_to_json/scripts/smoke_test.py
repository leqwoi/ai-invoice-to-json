from ai_invoice_to_json.evaluation.loader import load_ground_truth
from ai_invoice_to_json.evaluation.report import print_report
from ai_invoice_to_json.evaluation.scorer import score_invoice
from ai_invoice_to_json.extraction.extractor import extract_invoice
from ai_invoice_to_json.pipeline.loader import extract_text_from_invoice
from ai_invoice_to_json.utils.logging import configure_logging

configure_logging()

if __name__ == "__main__":
    document_id = "messy_invoice_1"
    document_path = f"dataset/invoices/{document_id}.pdf"
    document_truth_path = f"dataset/ground_truth/{document_id}.json"

    # prediction
    full_text = extract_text_from_invoice(document_path, document_id)
    predicted = extract_invoice(full_text, document_id)

    # ground truth
    ground_truth = load_ground_truth(document_truth_path)
    print(ground_truth)

    # scoring
    results = score_invoice(predicted, ground_truth)
    print_report(results, document_id)
