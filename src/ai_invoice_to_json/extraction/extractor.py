import openai
import structlog
from instructor.core import InstructorRetryException

from ai_invoice_to_json.exceptions import (
    ExtractionAPIError,
    ExtractionUnexpectedError,
    ExtractionValidationError,
)
from ai_invoice_to_json.extraction.client import get_llm_client
from ai_invoice_to_json.extraction.prompts import PROMPT_VERSION, SYSTEM_PROMPT
from ai_invoice_to_json.schema import Invoice

log = structlog.get_logger()


def extract_invoice(full_text: str, document_id: str) -> Invoice:
    log_ctx = log.bind(document_id=document_id, prompt_version=PROMPT_VERSION)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": full_text},
    ]

    client = get_llm_client()
    try:
        max_retries = 2
        resp, completion = client.create_with_completion(
            response_model=Invoice, messages=messages, max_retries=max_retries
        )  # ty:ignore[no-matching-overload]
        log_ctx.info(
            "extraction_succeeded",
            tokens_used=completion.usage,
        )
        return resp
    except InstructorRetryException as e:
        log_ctx.error(
            "extraction_validation_failed",
            error=str(e),
            max_retries=max_retries,
            exc_info=True,
        )
        raise ExtractionValidationError(
            f"Extraction failed after {max_retries} retries."
        ) from e
    except openai.BadRequestError as e:
        log_ctx.error("extraction_api_error", error=str(e), exc_info=True)
        raise ExtractionAPIError("LLM API Bad Request!") from e
    except Exception as e:
        log_ctx.error("extraction_unexpected_error", error=str(e), exc_info=True)
        raise ExtractionUnexpectedError(f"Unexpected error occurred: {e}") from e
