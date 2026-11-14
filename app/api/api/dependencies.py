from collections.abc import Generator
from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy.orm import Session

from core.security import get_current_user, get_current_user_id
from db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Database dependency
DbSession = Annotated[Session, Depends(get_db)]

# Authentication dependencies
CurrentUser = Annotated[
    dict[str, Any],
    Depends(get_current_user),
]

CurrentUserID = Annotated[
    str,
    Depends(get_current_user_id),
]
