from account.models import BlogUser
from account.api.serializers import BlogRegSerializer
from rest_framework import viewsets


class BlogRegViewSet(viewsets.ModelViewSet):
    queryset = BlogUser.objects.all()
    serializer_class = BlogRegSerializer
