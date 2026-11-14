import pytest
from sqlalchemy.orm import Session

from core.exceptions import AppException
from features.users.services import UserProfileService


def test_create_profile(db_session: Session) -> None:
    service = UserProfileService(db_session)

    profile = service.create_profile(
        auth_user_id="service-user-001",
        display_name="Service Test",
        phone_number="081234567890",
    )

    assert profile.auth_user_id == "service-user-001"
    assert profile.display_name == "Service Test"


def test_create_duplicate_profile(db_session: Session) -> None:
    service = UserProfileService(db_session)

    service.create_profile("service-user-002", "First User")

    with pytest.raises(AppException) as exc_info:
        service.create_profile("service-user-002", "Second User")

    assert exc_info.value.status_code == 409


def test_get_profile(db_session: Session) -> None:
    service = UserProfileService(db_session)
    service.create_profile("service-user-003", "Get Test")

    profile = service.get_profile("service-user-003")
    assert profile.display_name == "Get Test"


def test_get_nonexistent_profile(db_session: Session) -> None:
    service = UserProfileService(db_session)

    with pytest.raises(AppException) as exc_info:
        service.get_profile("unknown-service-user")

    assert exc_info.value.status_code == 404


def test_update_profile(db_session: Session) -> None:
    service = UserProfileService(db_session)
    service.create_profile("service-user-004", "Before")

    profile = service.update_profile(
        "service-user-004",
        {"display_name": "After"},
    )

    assert profile.display_name == "After"


def test_update_profile_rejects_empty_payload(
    db_session: Session,
) -> None:
    service = UserProfileService(db_session)
    service.create_profile("service-user-005", "Empty Test")

    with pytest.raises(AppException) as exc_info:
        service.update_profile("service-user-005", {})

    assert exc_info.value.status_code == 400


def test_update_profile_rejects_null_display_name(
    db_session: Session,
) -> None:
    service = UserProfileService(db_session)
    service.create_profile("service-user-006", "Null Test")

    with pytest.raises(AppException) as exc_info:
        service.update_profile(
            "service-user-006",
            {"display_name": None},
        )

    assert exc_info.value.status_code == 422


def test_delete_profile(db_session: Session) -> None:
    service = UserProfileService(db_session)
    service.create_profile("service-user-007", "Delete Test")

    service.delete_profile("service-user-007")

    with pytest.raises(AppException) as exc_info:
        service.get_profile("service-user-007")

    assert exc_info.value.status_code == 404
