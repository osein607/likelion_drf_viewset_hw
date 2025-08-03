from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
  # id = serializers.CharField(read_only=True) #2주차 20p
  tags = serializers.SerializerMethodField()
  image = serializers.ImageField(use_url=True, required=False)
  comments = serializers.SerializerMethodField(read_only=True)

  def get_comments(self, instance):
    serializer = CommentSerializer(instance.comments, many=True)
    return serializer.data

  def get_tags(self, instance):
    tag = instance.tags.all()
    return [t.name for t in tag]

  class Meta:
    model = Post
    fields = '__all__'
    read_only_fields = [
      "id",
      "created_at",
      "updated_at",
      "comments",
      "like_num"
    ]

class PostListSerializer(serializers.ModelSerializer):
  comments_cnt = serializers.SerializerMethodField()
  tags = serializers.SerializerMethodField()

  def get_comments_cnt(self, instance):
    return instance.comments.count()

  def get_tags(self, instance):
    tag = instance.tags.all()
    return [t.name for t in tag]
  
  class Meta:
    model = Post
    fields = [
      "id",
      "name",
      "created_at",
      "updated_at",
      "image",
      "comments_cnt",
      "tags",
      "like_num"
    ]
    read_only_fields = ["id", "created_at", "updated_at", "comments_cnt", "like_num"]

class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'
    read_only_fields = ['post'] # 유효성검사를 통과하기 위함
