from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, LessonViewSet, TagViewSet, MeView

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tag')
router.register('courses', CourseViewSet, basename='course')
router.register('lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('me/', MeView.as_view(), name='me'),
] + router.urls