from unittest import TestCase

from jwti.jwt import decode_jwt


FAKE_JWTS = {
    "basic": {
        "string": (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwi"
            "bmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.K"
            "MUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30"
        ),
        "dict": {
            "sub": "1234567890",
            "name": "John Doe",
            "admin": True,
            "iat": 1516239022
        }
    },
    "complex": {
        "string": (
          "eyJhbGciOiJQUzM4NCIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibm"
          "FtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMiwicm9sZ"
          "SI6ImFkbWluIiwiYWxsb3dlZF9pZHMiOlsxMiw0NSw3OF0sImRpY3QiOnsiY29tcGxl"
          "eCI6InR5cGUifX0.limRghV3fuszi9BTryH-2muG9gORwf_1XNxs4-_wgYVZ1NwCfkG"
          "ilsNpyXywTKus-zv4i0Mh0_XeAzmcCzNgz5c1YxLhw_cXogGpcNLnjQwxVom05mTuD-"
          "aL8-0PTgkGBVmK7UXxzIZXobwd_kyQJguNE46BeXqCJIRx8m5JNUEa_fwI5xRdDb8bk"
          "UaIuESJDRpgmRyNgqiGdR51ypvjTePDMU_zkOMucclyOBbDOutHj_a2bzj4CODOLxrp"
          "siPLZu0rxltp08kpkf8gVfFnJddp8KHX6-btgWaw0_vDQ4qQuVYHlq9U0ePQ6nnyTFr"
          "fSBLT2W5M7IABNr-hQICzoQ"
        ),
        "dict": {
            "sub": "1234567890",
            "name": "John Doe",
            "admin": True,
            "iat": 1516239022,
            "role": "admin",
            "allowed_ids": [12, 45, 78],
            "dict": {
                "complex": "type"
            }
        }
    }
}

GARBAGE_JWT_STRING_SHORT = "this.is.not.a.valid.jwt.token"
GARBAGE_JWT_STRING_LONG = (
    "this.is.not.a.valid.jwt.token.but.it.is.longer.than.the.minimum.length"
    ".so.it.will.not.raise.a.ValueError.but.it.will.raise.a.RuntimeError"
)
GARBAGE_JWT_STRING_ENCODING = (
    "UzI1NiIsInIkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0."
    "eyJhbGciOiJIR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6"
    "GM6H9FNFUROf3wh7SmqJp-QV30"
)


class TestJwt(TestCase):
    """Unit tests for jwt functions."""

    def test_decode_jwt_positive(self) -> dict:
        """Supported cases by decode_jwt()."""
        for jwt in FAKE_JWTS.values():
            string_jwt = jwt["string"]
            dict_jwt = jwt["dict"]

            decoded_jwt = decode_jwt(string_jwt)
            self.assertIsInstance(decoded_jwt, dict)

            for claim in dict_jwt.items():
                claim_name = claim[0]
                claim_value = claim[1]
                self.assertEqual(claim_value, decoded_jwt.get(claim_name))

    def test_decode_jwt_negative(self) -> dict:
        """Things that should cause decode_jwt() to fail."""
        with self.assertRaises(ValueError):
            decode_jwt(2)

        with self.assertRaises(ValueError):
            decode_jwt(GARBAGE_JWT_STRING_SHORT)

        with self.assertRaises(RuntimeError):
            decode_jwt(GARBAGE_JWT_STRING_LONG)

        with self.assertRaises(RuntimeError):
            decode_jwt(GARBAGE_JWT_STRING_ENCODING)
