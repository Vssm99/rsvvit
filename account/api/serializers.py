from account.models import BlogUser
from rest_framework import serializers


class BlogRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogUser
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email', 'city', 'country', 'gender', 'profile_image']
