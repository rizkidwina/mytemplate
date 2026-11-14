from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserProfileCreate(BaseModel):
    display_name: str = Field(
        min_length=1,
        max_length=100,
    )

    phone_number: str | None = Field(
        default=None,
        max_length=20,
    )


class UserProfileUpdate(BaseModel):
    display_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    phone_number: str | None = Field(
        default=None,
        max_length=20,
    )


class UserProfileResponse(BaseModel):
    id: UUID
    auth_user_id: str
    display_name: str
    phone_number: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
