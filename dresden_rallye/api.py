from rest_framework.routers import DefaultRouter

from user.urls import router as user_router

router = DefaultRouter()

router.registry.extend(user_router.registry)