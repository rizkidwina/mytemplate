from fastapi import APIRouter

from features.users.endpoints import router as users_router

api_router = APIRouter()


@api_router.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "version": "v1",
    }


api_router.include_router(
    users_router,
    prefix="/users",
    tags=["Users"],
)
