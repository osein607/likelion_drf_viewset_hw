from django.db import models

# Create your models here.
class Tag(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=50)

def image_upload_path(instance, filename):
  return f'{instance.pk}/{filename}'

class Post(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=50)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True) #생성일자
  updated_at = models.DateTimeField(auto_now=True) #수정일자
  tags = models.ManyToManyField(Tag, blank=True)
  image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)
  like_num = models.PositiveSmallIntegerField(default=0)

class Comment(models.Model):
  id = models.AutoField(primary_key=True)
  post = models.ForeignKey(Post, blank=False, null=False, on_delete=models.CASCADE, related_name='comments') #역참조로 포스트의 댓글을 불러오도록
  writer = models.CharField(max_length=50)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)