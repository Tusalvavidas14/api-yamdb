from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    get_token,
    signup,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='token'),
    path(
        'titles/<int:title_id>/reviews/',
        ReviewViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='reviews-list',
    ),
    path(
        'titles/<int:title_id>/reviews/<int:pk>/',
        ReviewViewSet.as_view(
            {'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}
        ),
        name='reviews-detail',
    ),
    path(
        'titles/<int:title_id>/reviews/<int:review_id>/comments/',
        CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='comments-list',
    ),
    path(
        'titles/<int:title_id>/reviews/<int:review_id>/comments/<int:pk>/',
        CommentViewSet.as_view(
            {'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}
        ),
        name='comments-detail',
    ),
    path('', include(router.urls)),
]
