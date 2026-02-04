from fastapi import APIRouter

from .products.views import router as product_router
from .demo_auth.views import router as demo_auth_router
from .auth.auth import router as auth_router

router = APIRouter()
router.include_router(
    router=product_router,
    prefix="/products",
)
router.include_router(
    router=demo_auth_router,
    prefix="/demo_auth",
)

router.include_router(
    router=auth_router,
    prefix="/real_auth",
)
