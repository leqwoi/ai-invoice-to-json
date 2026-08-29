from pathlib import Path

import pdfplumber
import structlog
from pdfminer.pdfdocument import PDFPasswordIncorrect
from pdfminer.pdfparser import PDFSyntaxError

from ai_invoice_to_json.exceptions import (
    ExtractionInputError,
    ExtractionUnexpectedError,
)

log = structlog.get_logger()


def extract_text_from_invoice(file_path: str | Path, document_id: str):
    log_ctx = log.bind(document_id=document_id, file_path=file_path)
    full_text = []

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text.append(text)
        log_ctx.info(
            "pdf_extraction_succeeded",
            pages_count=len(full_text),
        )
    except FileNotFoundError as e:
        log_ctx.error("extraction_input_error", error=str(e), exc_info=True)
        raise ExtractionInputError(f"Invoice file not found: {file_path}") from e
    except PermissionError as e:
        log_ctx.error("extraction_input_error", error=str(e), exc_info=True)
        raise ExtractionInputError(f"Access denied. Cannot read {file_path}") from e
    except PDFSyntaxError as e:
        log_ctx.error("extraction_input_error", error=str(e), exc_info=True)
        raise ExtractionInputError(
            f"{file_path} is corrupted, empty, or not a valid PDF."
        ) from e
    except PDFPasswordIncorrect as e:
        log_ctx.error("extraction_input_error", error=str(e), exc_info=True)
        raise ExtractionInputError(
            f"{file_path} is encrypted. A valid password is required."
        ) from e
    except Exception as e:
        log_ctx.error("extraction_unexpected_error", error=str(e))
        raise ExtractionUnexpectedError(f"Unexpected error occurred: {e}") from e

    if len(full_text) == 0:
        log_ctx.error(
            "extraction_input_error",
            error="No extractable text found (scanned/image-based PDF)",
            file_path=file_path,
            exc_info=True,
        )
        raise ExtractionInputError(
            f"No extractable text found in {file_path} — likely a scanned/image-based PDF."
        )

    return "\n".join(full_text)
