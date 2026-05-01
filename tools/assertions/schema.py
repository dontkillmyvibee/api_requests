from typing import Any

import allure
from jsonschema import validate
from jsonschema.validators import Draft202012Validator

from tools.logger import get_logger

logger = get_logger("SCHEMA_ASSERTIONS")


@allure.step("Validating JSON schema")
def validate_json_schema(instance: Any, schema: dict) -> None:
    """

    Args:
        instance: JSON-данные, которые нужно проверить.
        schema: Ожидаемая JSON-schema.

    Raises:
        jsonschema.exceptions.ValidationError: Если instance не соответствует schema.

    """
    logger.info("Validating JSON schema")

    validate(
        schema=schema,
        instance=instance,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )