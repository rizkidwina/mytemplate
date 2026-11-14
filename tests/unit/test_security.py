import time

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jwt.exceptions import PyJWKClientError

import core.security as security
from core.config import settings


class FakeSigningKey:
    def __init__(self, key: object) -> None:
        self.key = key


class FakeJWKClient:
    def __init__(self, public_key: object) -> None:
        self.public_key = public_key

    def get_signing_key_from_jwt(self, token: str) -> FakeSigningKey:
        return FakeSigningKey(self.public_key)


def make_credentials(token: str) -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )


def make_token(
    private_key: Ed25519PrivateKey,
    **overrides: object,
) -> str:
    now = int(time.time())

    payload: dict[str, object] = {
        "sub": "test-auth-user-001",
        "iss": settings.AUTH_ISSUER,
        "aud": settings.AUTH_AUDIENCE,
        "iat": now,
        "exp": now + 300,
    }

    payload.update(overrides)

    return jwt.encode(
        payload,
        private_key,
        algorithm=settings.AUTH_JWT_ALGORITHM,
    )


@pytest.fixture
def signing_keys() -> tuple[Ed25519PrivateKey, Ed25519PrivateKey]:
    return (
        Ed25519PrivateKey.generate(),
        Ed25519PrivateKey.generate(),
    )


def test_get_current_user_with_valid_token(
    monkeypatch: pytest.MonkeyPatch,
    signing_keys: tuple[Ed25519PrivateKey, Ed25519PrivateKey],
) -> None:
    private_key, _ = signing_keys

    monkeypatch.setattr(
        security,
        "get_jwks_client",
        lambda: FakeJWKClient(private_key.public_key()),
    )

    token = make_token(private_key)
    result = security.get_current_user(make_credentials(token))

    assert result["sub"] == "test-auth-user-001"


def test_get_current_user_without_credentials() -> None:
    with pytest.raises(HTTPException) as exc:
        security.get_current_user(None)

    assert exc.value.status_code == 401


def test_get_current_user_with_invalid_signature(
    monkeypatch: pytest.MonkeyPatch,
    signing_keys: tuple[Ed25519PrivateKey, Ed25519PrivateKey],
) -> None:
    private_key, other_private_key = signing_keys

    monkeypatch.setattr(
        security,
        "get_jwks_client",
        lambda: FakeJWKClient(private_key.public_key()),
    )

    token = make_token(other_private_key)

    with pytest.raises(HTTPException) as exc:
        security.get_current_user(make_credentials(token))

    assert exc.value.status_code == 401


def test_get_current_user_with_expired_token(
    monkeypatch: pytest.MonkeyPatch,
    signing_keys: tuple[Ed25519PrivateKey, Ed25519PrivateKey],
) -> None:
    private_key, _ = signing_keys

    monkeypatch.setattr(
        security,
        "get_jwks_client",
        lambda: FakeJWKClient(private_key.public_key()),
    )

    token = make_token(
        private_key,
        exp=int(time.time()) - 60,
        iat=int(time.time()) - 120,
    )

    with pytest.raises(HTTPException) as exc:
        security.get_current_user(make_credentials(token))

    assert exc.value.status_code == 401


@pytest.mark.parametrize(
    ("claim", "value"),
    [
        ("iss", "https://wrong-issuer.example"),
        ("aud", "https://wrong-audience.example"),
    ],
)
def test_get_current_user_with_invalid_claims(
    monkeypatch: pytest.MonkeyPatch,
    signing_keys: tuple[Ed25519PrivateKey, Ed25519PrivateKey],
    claim: str,
    value: str,
) -> None:
    private_key, _ = signing_keys

    monkeypatch.setattr(
        security,
        "get_jwks_client",
        lambda: FakeJWKClient(private_key.public_key()),
    )

    token = make_token(private_key, **{claim: value})

    with pytest.raises(HTTPException) as exc:
        security.get_current_user(make_credentials(token))

    assert exc.value.status_code == 401


def test_get_current_user_with_empty_subject(
    monkeypatch: pytest.MonkeyPatch,
    signing_keys: tuple[Ed25519PrivateKey, Ed25519PrivateKey],
) -> None:
    private_key, _ = signing_keys

    monkeypatch.setattr(
        security,
        "get_jwks_client",
        lambda: FakeJWKClient(private_key.public_key()),
    )

    token = make_token(private_key, sub="")

    with pytest.raises(HTTPException) as exc:
        security.get_current_user(make_credentials(token))

    assert exc.value.status_code == 401


def test_get_current_user_when_jwks_is_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class UnavailableJWKClient:
        def get_signing_key_from_jwt(self, token: str) -> None:
            raise PyJWKClientError("JWKS unavailable")

    monkeypatch.setattr(
        security,
        "get_jwks_client",
        lambda: UnavailableJWKClient(),
    )

    with pytest.raises(HTTPException) as exc:
        security.get_current_user(make_credentials("some-token"))

    assert exc.value.status_code == 503
