from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import CreateUserAPIView, MyTokenObtainPairView, UserViewSet
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    url('auth/email/', CreateUserAPIView.as_view()),
    path('token/', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
