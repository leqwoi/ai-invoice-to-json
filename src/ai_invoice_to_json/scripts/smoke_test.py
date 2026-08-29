from ai_invoice_to_json.extraction.extractor import extract_invoice
from ai_invoice_to_json.pipeline.loader import extract_text_from_invoice
from ai_invoice_to_json.utils.logging import configure_logging

configure_logging()

if __name__ == "__main__":
    document_id = "invoice_10474.pdf"
    full_text = extract_text_from_invoice(
        f"dataset/invoices/{document_id}", document_id
    )
    invoice = extract_invoice(full_text, document_id)

    print("\nResult:")
    print(invoice.model_dump())
