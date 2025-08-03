from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import viewsets, mixins

from .models import *
from .serializers import *

import re

from django.shortcuts import get_object_or_404

# 특정 태그를 포함한 게시물 목록 불러오기
class TagViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer
  lookup_field = "name" #태그 객체 조회 시 사용할 필드 설정
  lookup_url_kwarg = "tag_name" #url 매개변수에서 실제 태그 이름을 나타내는 매개변수 이름 설정

  def retrieve(self, request, *args, **kwargs): #전체가 아닌 디테일이니까 retrieve
    tag_name = kwargs.get("tag_name") #url 매개변수 tag_name에서 실제 태그 이름을 가져온다
    tags = get_object_or_404(Tag, name=tag_name) #Tag 모델에서 name=tag_name인 태그 객체 가져옴
    posts = Post.objects.filter(tags=tags) #Post 모델에서 tag와 일치하는 post 객체 필터링
    serializer = PostSerializer(posts, many=True) #post시리얼라이저로 직렬화
    return Response(serializer.data)

# 게시물 리스트 조회 수정 삭제
class PostViewSet(viewsets.ModelViewSet):
  queryset = Post.objects.all()
  # serializer_class = PostSerializer

  def get_serializer_class(self):
    if (self.action == "list" or self.action == "top3_liked") :
      return PostListSerializer
    return PostSerializer

  def create(self, request): #db에 저장할 때 반드시 필요한 필드는 perform_create말고 create
    serializer = self.get_serializer(data=request.data) #요청데이터를 기반으로 시리얼라이저 생성
    serializer.is_valid(raise_exception=True) #시리얼라이저 유효성 검사
    self.perform_create(serializer) #받은 시리얼라이저를 이용하여 post 객체 생성

    post = serializer.instance #생성된 객체를 가져와서 post 변수에 저장
    self.handle_tags(post) #새로 구현한 handle_tags 함수를 이용하기 위한 코드

    return Response(serializer.data) #생성된 post 객체 데이터를 응답으로 반환
  
  def perform_update(self, serializer):
    post = serializer.save()
    post.tags.clear()
    self.handle_tags(post)
  
  def handle_tags(self, post):
    words = re.split(r'[\s,]+', post.content.strip())
    tag_list = []
    for w in words:
      if len(w) > 0:
        if w[0] == '#':
          tag_list.append(w[1:])
    for t in tag_list:
      tag, _ = Tag.objects.get_or_create(name=t)
      post.tags.add(tag)
    post.save()

  # 좋아요 상위 3개 포스트 반환
  @action(methods=["GET"], detail=False)
  def top3_liked(self, request):
    top_post = self.get_queryset().order_by("-like_num")[:3]
    top_post_serializer = PostListSerializer(top_post, many=True)
    return Response(top_post_serializer.data)

  # 요청마다 각 포스트의 like_num += 1
  @action(methods=["GET"], detail=True)
  def test(self, request, pk=None):
    test_post = self.get_object()
    test_post.like_num += 1
    test_post.save(update_fields=["like_num"])
    return Response()

# 댓글 디테일 조회 수정 삭제, 모든 mixin이 아니므로 제네릭 상속
class CommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer
  
# 게시물의 댓글 목록 조회, 게시물에 댓글 작성
class PostCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
  # queryset = Comment.objects.all()
  serializer_class = CommentSerializer #모든 액션에 대해 동일한 시리얼라이저 적용

  # def list(self, request, post_id = None):
  #   post = get_object_or_404(Post, id=post_id) #Post 모델에서 id에 해당하는 객체를 불러옴
  #   queryset = self.filter_queryset(self.get_queryset().filter(post=post)) #쿼리셋을 post에 해당하는 것으로 필터링
  #   serializer = self.get_serializer(queryset, many=True) #쿼리셋 직렬화, many=True
  #   return Response(serializer.data)
  
  def get_queryset(self):
    post = self.kwargs.get("post_id") #url에서 추출된 post_id를 가져오는 코드
    queryset = Comment.objects.filter(post_id=post) #id에 해당하는 게시물에 대한 댓글만 필터링하여 반환
    return queryset


  def create(self, request, post_id = None):
    post = get_object_or_404(Post, id=post_id)
    serializer = self.get_serializer(data = request.data)
    serializer.is_valid(raise_exception=True) #시리얼라이저 유효성검사
    serializer.save(post=post)
    return Response(serializer.data)
  