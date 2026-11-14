from sqlalchemy import select
from sqlalchemy.orm import Session

from features.users.models import UserProfile


class UserProfileRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_auth_user_id(
        self,
        auth_user_id: str,
    ) -> UserProfile | None:
        statement = select(UserProfile).where(UserProfile.auth_user_id == auth_user_id)

        return self.db.scalar(statement)

    def create(
        self,
        auth_user_id: str,
        display_name: str,
        phone_number: str | None = None,
    ) -> UserProfile:
        profile = UserProfile(
            auth_user_id=auth_user_id,
            display_name=display_name,
            phone_number=phone_number,
        )

        self.db.add(profile)
        self.db.flush()
        self.db.refresh(profile)

        return profile

    def update(
        self,
        profile: UserProfile,
        data: dict[str, object],
    ) -> UserProfile:
        for field, value in data.items():
            setattr(profile, field, value)

        self.db.flush()
        self.db.refresh(profile)

        return profile

    def delete(self, profile: UserProfile) -> None:
        self.db.delete(profile)
        self.db.flush()
