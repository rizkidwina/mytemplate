import pytest
from pydantic import ValidationError

from features.users.schemas import UserProfileCreate, UserProfileUpdate


def test_create_profile_with_valid_data() -> None:
    data = UserProfileCreate(
        display_name="Test User",
        phone_number="081234567890",
    )
    assert data.display_name == "Test User"
    assert data.phone_number == "081234567890"


def test_create_profile_without_phone_number() -> None:
    data = UserProfileCreate(display_name="Test User")
    assert data.phone_number is None


def test_create_profile_rejects_empty_display_name() -> None:
    with pytest.raises(ValidationError):
        UserProfileCreate(display_name="")


def test_create_profile_rejects_long_display_name() -> None:
    with pytest.raises(ValidationError):
        UserProfileCreate(display_name="A" * 101)


def test_create_profile_rejects_long_phone_number() -> None:
    with pytest.raises(ValidationError):
        UserProfileCreate(
            display_name="Test User",
            phone_number="1" * 21,
        )


def test_update_profile_with_partial_data() -> None:
    data = UserProfileUpdate(display_name="Updated User")
    assert data.model_dump(exclude_unset=True) == {"display_name": "Updated User"}


def test_update_profile_can_clear_phone_number() -> None:
    data = UserProfileUpdate(phone_number=None)
    assert data.model_dump(exclude_unset=True) == {"phone_number": None}


def test_update_profile_empty_payload() -> None:
    data = UserProfileUpdate()
    assert data.model_dump(exclude_unset=True) == {}
