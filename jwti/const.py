from os import getenv

LOG_LEVEL = "DEBUG" if getenv("DEBUG") == "1" else "INFO"
TOKEN_MIN_LENGTH = 40
TOKEN_PEEK_CHARS = 6   # Smaller than 2x TOKEN_MIN_LENGTH
JWT_REGISTERED_CLAIMS = {
    "iss": "issuer",
    "sub": "subject",
    "aud": "audience",
    "exp": "expiration",
    "iat": "issued-at",
    "nbf": "not-before",
    "jti": "token-id"
}
JWT_DATE_CLAIMS = ["exp", "iat", "nbf"]
