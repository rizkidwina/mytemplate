from fastapi import APIRouter, Response, status

from api.dependencies import CurrentUserID, DbSession
from features.users.models import UserProfile
from features.users.schemas import (
    UserProfileCreate,
    UserProfileResponse,
    UserProfileUpdate,
)
from features.users.services import UserProfileService

router = APIRouter()


@router.post(
    "/me/profile",
    response_model=UserProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_my_profile(
    data: UserProfileCreate,
    db: DbSession,
    auth_user_id: CurrentUserID,
) -> UserProfile:
    service = UserProfileService(db)

    return service.create_profile(
        auth_user_id=auth_user_id,
        display_name=data.display_name,
        phone_number=data.phone_number,
    )


@router.get(
    "/me/profile",
    response_model=UserProfileResponse,
)
def get_my_profile(
    db: DbSession,
    auth_user_id: CurrentUserID,
) -> UserProfile:
    service = UserProfileService(db)

    return service.get_profile(auth_user_id)


@router.patch(
    "/me/profile",
    response_model=UserProfileResponse,
)
def update_my_profile(
    data: UserProfileUpdate,
    db: DbSession,
    auth_user_id: CurrentUserID,
) -> UserProfile:
    service = UserProfileService(db)

    return service.update_profile(
        auth_user_id=auth_user_id,
        data=data.model_dump(exclude_unset=True),
    )


@router.delete(
    "/me/profile",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_my_profile(
    db: DbSession,
    auth_user_id: CurrentUserID,
) -> Response:
    service = UserProfileService(db)
    service.delete_profile(auth_user_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
