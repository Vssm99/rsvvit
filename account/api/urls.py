from django.urls import path, include
from account.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('reg', views.BlogRegViewSet, basename='register')
urlpatterns = [
    path('', include(router.urls))
]
