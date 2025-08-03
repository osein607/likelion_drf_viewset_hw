from django.urls import path, include
from rest_framework import routers
from .views import *

from django.conf.urls.static import static
from django.conf import settings

app_name = "post"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("posts", PostViewSet, basename="posts")

comment_router = routers.SimpleRouter(trailing_slash=False)
comment_router.register("comments", CommentViewSet, basename="comments")

post_comment_router = routers.SimpleRouter(trailing_slash=False)
post_comment_router.register("comments", PostCommentViewSet, basename="comments")

tag_router = routers.SimpleRouter(trailing_slash=False)
tag_router.register("tags", TagViewSet, basename="tags")

urlpatterns = [
    path("", include(default_router.urls)),
    path("", include(comment_router.urls)),
    path("posts/<int:post_id>/", include(post_comment_router.urls)), #게시물의 댓글을 불러오고 작성하는 거기 때문!
    path("", include(tag_router.urls)),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
