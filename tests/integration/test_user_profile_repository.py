from sqlalchemy.orm import Session

from features.users.repositories import UserProfileRepository


def test_create_and_get_profile(db_session: Session) -> None:
    repository = UserProfileRepository(db_session)

    profile = repository.create(
        auth_user_id="repository-user-001",
        display_name="Repository Test",
        phone_number="081234567890",
    )
    db_session.commit()

    result = repository.get_by_auth_user_id("repository-user-001")

    assert result is not None
    assert result.id == profile.id
    assert result.display_name == "Repository Test"


def test_get_nonexistent_profile(db_session: Session) -> None:
    repository = UserProfileRepository(db_session)
    assert repository.get_by_auth_user_id("unknown-user") is None


def test_update_profile(db_session: Session) -> None:
    repository = UserProfileRepository(db_session)

    profile = repository.create(
        auth_user_id="repository-user-002",
        display_name="Before Update",
    )

    repository.update(profile, {"display_name": "After Update"})
    db_session.commit()

    result = repository.get_by_auth_user_id("repository-user-002")
    assert result is not None
    assert result.display_name == "After Update"


def test_delete_profile(db_session: Session) -> None:
    repository = UserProfileRepository(db_session)

    profile = repository.create(
        auth_user_id="repository-user-003",
        display_name="Delete Test",
    )
    db_session.commit()

    repository.delete(profile)
    db_session.commit()

    assert repository.get_by_auth_user_id("repository-user-003") is None
