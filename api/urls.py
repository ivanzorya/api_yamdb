from django.urls import path, include
from rest_framework.routers import SimpleRouter, Route, DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (CreateUserAPIView, MyTokenObtainPairView, UserViewSet,
                    APIUserDetail, ReviewViewSet, CategoryViewSet,
                    TitleViewSet, CommentViewSet, GenreViewSet)


class CustomUserRouter(SimpleRouter):
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


class CustomCategoryGenreRouter(SimpleRouter):
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


router_category_genre = CustomCategoryGenreRouter()
router_category_genre.register(r'categories', CategoryViewSet)
router_category_genre.register(r'genres', GenreViewSet)

router_user = CustomUserRouter()
router_user.register(r'users', UserViewSet)

router_review_comment_title = DefaultRouter()
router_review_comment_title.register(r'titles', TitleViewSet)
router_review_comment_title.register(
    r'titles/(?P<title_id>[^/.]+)/reviews',
    ReviewViewSet
)
router_review_comment_title.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet
)


urlpatterns = [
    path('v1/users/me/', APIUserDetail.as_view()),
    path('v1/', include(router_user.urls)),
    path('v1/', include(router_review_comment_title.urls)),
    path('v1/', include(router_category_genre.urls)),
    path('v1/auth/email/', CreateUserAPIView.as_view()),
    path('v1/token/', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
