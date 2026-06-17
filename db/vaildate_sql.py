import sqlglot
from sqlglot import exp

from config.settings import get_config
from db.allowlist import ALLOWED_TABLES
from utils.logger import get_logger

logger = get_logger(__name__)

FORBIDDEN_KEYWORDS = frozenset(  # new code
    {"insert", "update", "delete", "drop", "alter", "truncate", "create", "grant", "revoke"}  # new code
)

class SqlValidationError(ValueError):
    """Custom exception for SQL validation errors."""

def normalize_sql(sql: str) -> str:
    """Normalize SQL by removing extra whitespace and formatting."""
    return sqlglot.strip().rstrip(';')

def validate_sql(sql: str, max_limit: int | None = None) -> str:
    if max_limit is None:
        max_limit = get_config().sql_max_limit

    cleaned = normalize_sql(sql)

    lowered = cleaned.lower()

    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in lowered:
            raise SqlValidationError(f"Forbidden SQL keyword detected: '{keyword}'")
        
    try:
        expression = sqlglot.parse_one(cleaned, dialect="postgres")
    except sqlglot.errors.ParseError as e:
        raise SqlValidationError(f"SQL parsing error: {e}") from e

    if not isinstance(expression, exp.Select):
        raise SqlValidationError("Only SELECT statements are allowed.")

    tables = {t.name.lower() for t in expression.find_all(exp.Table)}

    limit_node = expression.args.get("limit")
    if limit_node is not None:
        try:
            value = int(limit_node.this.name)
        except (ValueError, AttributeError) as e:
            raise SqlValidationError("Invalid LIMIT value.")
        
    if value < 0:
        raise SqlValidationError(f"LIMIT must be non-negative, got {value}.")
    
    if value > max_limit:
        value = max_limit

    logger.info("SQL OK")

    return cleaned