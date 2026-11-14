from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.exceptions import AppException
from features.users.models import UserProfile
from features.users.repositories import UserProfileRepository


class UserProfileService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = UserProfileRepository(db)

    def get_profile(self, auth_user_id: str) -> UserProfile:
        profile = self.repository.get_by_auth_user_id(auth_user_id)

        if profile is None:
            raise AppException(
                status_code=404,
                detail="User profile not found",
                code="USER_PROFILE_NOT_FOUND",
            )

        return profile

    def create_profile(
        self,
        auth_user_id: str,
        display_name: str,
        phone_number: str | None = None,
    ) -> UserProfile:
        existing = self.repository.get_by_auth_user_id(auth_user_id)

        if existing is not None:
            raise AppException(
                status_code=409,
                detail="User profile already exists",
                code="USER_PROFILE_ALREADY_EXISTS",
            )

        try:
            profile = self.repository.create(
                auth_user_id=auth_user_id,
                display_name=display_name,
                phone_number=phone_number,
            )

            self.db.commit()
            self.db.refresh(profile)

            return profile

        except IntegrityError as exc:
            self.db.rollback()
            raise AppException(
                status_code=409,
                detail="User profile already exists",
                code="USER_PROFILE_ALREADY_EXISTS",
            ) from exc

    def update_profile(
        self,
        auth_user_id: str,
        data: dict[str, object],
    ) -> UserProfile:
        profile = self.get_profile(auth_user_id)

        if not data:
            raise AppException(
                status_code=400,
                detail="No fields provided for update",
                code="EMPTY_UPDATE",
            )

        if "display_name" in data and data["display_name"] is None:
            raise AppException(
                status_code=422,
                detail="Display name cannot be null",
                code="INVALID_DISPLAY_NAME",
            )

        try:
            profile = self.repository.update(profile, data)

            self.db.commit()
            self.db.refresh(profile)

            return profile

        except Exception:
            self.db.rollback()
            raise

    def delete_profile(self, auth_user_id: str) -> None:
        profile = self.get_profile(auth_user_id)

        try:
            self.repository.delete(profile)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise
