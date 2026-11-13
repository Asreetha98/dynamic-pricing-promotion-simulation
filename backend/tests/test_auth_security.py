from app.utils.security import hash_password, verify_password, create_access_token, decode_access_token


def test_password_hash_and_verify():
    hashed = hash_password("StrongPass123!")
    assert hashed != "StrongPass123!"
    assert verify_password("StrongPass123!", hashed)
    assert not verify_password("WrongPass123!", hashed)


def test_jwt_round_trip():
    token = create_access_token("123")
    payload = decode_access_token(token)
    assert payload["sub"] == "123"
