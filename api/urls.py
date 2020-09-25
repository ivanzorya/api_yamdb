from django.urls import include, path
from rest_framework.routers import Route, SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CategoryViewSet, GenreViewSet


class CustomCategoryRouter(SimpleRouter):
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
            mapping={'delete': 'destroy',
                     },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
    ]


v1_router = CustomCategoryRouter()
v1_router.register(r'categories', CategoryViewSet)
v1_router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        'v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
