from jwt import DecodeError, decode as jwt_decode
from datetime import datetime

from jwti.const import TOKEN_PEEK_CHARS, TOKEN_MIN_LENGTH, JWT_DATE_CLAIMS
from jwti.logger import log


def decode_jwt(
        jwt: str, algorithms: list = None,
        verify_signature: bool = False
) -> dict:
    """Decode a JWT token and parse it as a dictionary."""
    if not jwt or len(jwt) < TOKEN_MIN_LENGTH:
        raise ValueError("Invalid token length.")

    token_peek = f"{jwt[0:TOKEN_PEEK_CHARS]}...{jwt[-TOKEN_PEEK_CHARS:]}'"
    log.debug(f"Inspecting token '{token_peek}'")

    try:
        payload = jwt_decode(
            jwt, algorithms=algorithms,
            options={"verify_signature": verify_signature}
        )
    except DecodeError as e:
        raise RuntimeError(f"Error decoding JWT '{token_peek}': {e}")
    except Exception as e:
        raise RuntimeError(
            f"Unexpected error decoding JWT '{token_peek}': {e}."
        )

    return payload


def parse_jwt_date_claims(jwt: dict) -> dict:
    """Parse the Unix timestamps in the JWT registered claims as dates"""
    for claim in JWT_DATE_CLAIMS:
        if jwt.get(claim):
            try:
                jwt[claim] = datetime.fromtimestamp(jwt[claim]).isoformat()
            except Exception:
                log.debug(f"Claim '{claim}' is not a unix a timestamp.")

    return jwt
