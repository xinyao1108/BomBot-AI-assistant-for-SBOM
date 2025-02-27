from fastapi import APIRouter
from app.api.routes import context
from app.api.routes import privacy
from app.api.routes import store

router = APIRouter()

router.include_router(context.router, prefix="/context")
router.include_router(privacy.router, prefix="")
router.include_router(store.router, prefix="/store")