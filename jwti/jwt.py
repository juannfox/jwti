from jwt import DecodeError, decode as jwt_decode
from datetime import datetime

from jwti.const import (
    TOKEN_PEEK_CHARS, TOKEN_MIN_LENGTH, JWT_DATE_CLAIMS, JWT_REGISTERED_CLAIMS
)
from jwti.logger import log


def decode_jwt(
        jwt: str, algorithms: list = None,
        verify_signature: bool = False
) -> dict:
    """Decode a JWT token and parse it as a dictionary."""
    if not jwt or not isinstance(jwt, str) or len(jwt) < TOKEN_MIN_LENGTH:
        raise ValueError("Invalid token.")

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


def parse_jwt_registered_claims(jwt: dict) -> dict:
    """Parse the Unix timestamps in the JWT registered claims as dates"""
    for claim in JWT_REGISTERED_CLAIMS.keys():
        if claim in jwt.keys():
            if claim in JWT_DATE_CLAIMS:
                try:
                    jwt[claim] = datetime.fromtimestamp(jwt[claim]).isoformat()
                except Exception:
                    log.debug(f"Claim '{claim}' is not a unix a timestamp.")

            claim_name = JWT_REGISTERED_CLAIMS[claim].capitalize()
            jwt[claim_name] = jwt.pop(claim)

    return jwt


def filter_jwt_claims(jwt: dict, claims: list) -> dict:
    """Filter the JWT claims to only include the specified ones."""
    filtered_jwt = {}
    for claim in claims:
        if claim in jwt.keys():
            filtered_jwt[claim] = jwt[claim]
        else:
            log.warning(f"Claim '{claim}' not found in JWT.")

    return filtered_jwt
