from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from jwcrypto import jwk

def pem_to_jwk(pem_key):
    # Load the public key from PEM format
    public_key = serialization.load_pem_public_key(
        pem_key.encode('utf-8'),
        backend=default_backend()
    )

    # Convert to JWK format
    jwk_key = jwk.JWK.from_pem(pem_key.encode('utf-8'))

    # Need to add alg to JWK otherwise KrakenD fails
    jwk_key["alg"] = "RS256"
    jwk_key["kid"] = "yourcoolkid"
    
    # Return the JWK as a JSON string
    return jwk_key.export()

# Example usage
pem_public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxM6n3q6oa58kcSv3Z0bd
obE+088FT7u8DyICNFt0xj6KQmjaA+oCOxnSFhWhhzo5DDURcFgplYx2XllG9ujF
xFIbC6+F0a+8d3Zm5jAyRGCwjPgO1JfHyrZ7V3DnrWqTSgsgBQ9I7Fhy2+HB5lU4
1IcBf4NP82Gp2Y6oA7N8pBDRpiC/1+LNpMcvcSyp5o1k4hzVfWJx9wsWYPeQdjL6
ijSQ5YQBu1bHNFzbPATl1d8j0TAEDxVK/c2K6eDgxDalMTgUWeaAMQww3S+NtrIZ
RsC6dmQm/XRVhy+2fofXG0bSMx5pDyuaaBQbcCjJMbRCYgX52nn7oOSMqdKciheO
SwIDAQAB
-----END PUBLIC KEY-----"""

jwk_public_key = pem_to_jwk(pem_public_key)
print(jwk_public_key)
