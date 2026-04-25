from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, CommentViewSet, GenreViewSet,
    ReviewViewSet, TitleViewSet, UserViewSet,
    get_token, signup
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')

reviews_router = DefaultRouter()
reviews_router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

comments_router = DefaultRouter()
comments_router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='token'),
    path('', include(router.urls)),
    path('', include(reviews_router.urls)),
    path('', include(comments_router.urls)),
]