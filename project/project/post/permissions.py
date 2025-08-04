from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
  def has_permission(self, request, view):
    return request.user and request.user.is_authenticated #존재하고, 인증된 사용자면 요청허용
  
  def has_object_permission(self, request, view, obj):
    if request.method in SAFE_METHODS: #요청 메서드가 SAFE 메서드 중 하나면 요청 허용
      return True
    return obj.writer == request.user or request.user.is_superuser #그 외는 작성자=요청사용자, 사용자=슈퍼유저인 경우 요청 허용
  