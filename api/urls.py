from django.urls import path, include
from rest_framework.routers import SimpleRouter, Route
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import CreateUserAPIView, MyTokenObtainPairView, UserViewSet, \
    APIUserDetail


class CustomRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={'get': 'list',
                     'post': 'create',
                     },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/$',
            mapping={'get': 'retrieve',
                     'patch': 'partial_update',
                     'delete': 'destroy',
                     },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
    ]


router = CustomRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('users/me/', APIUserDetail.as_view()),
    path('', include(router.urls)),
    path('auth/email/', CreateUserAPIView.as_view()),
    path('token/', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
