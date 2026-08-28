from functools import lru_cache

import instructor
from instructor.core import Instructor

from ai_invoice_to_json.config import get_settings


@lru_cache
def get_llm_client() -> Instructor:
    settings = get_settings()

    return instructor.from_provider(
        f"{settings.llm_provider}/{settings.llm_model}",
        base_url=settings.base_url,
        api_key=settings.api_key.get_secret_value(),
    )
