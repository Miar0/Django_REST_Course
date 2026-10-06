from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, LessonViewSet, TagViewSet

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tag')
router.register('courses', CourseViewSet, basename='course')
router.register('lessons', LessonViewSet, basename='lesson')

urlpatterns = router.urls