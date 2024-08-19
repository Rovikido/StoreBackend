from django.urls import path, include
from backend.urls import router as backend_router

urlpatterns = [
    path('', include(backend_router.urls)),
]