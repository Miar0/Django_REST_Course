from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),

    path('lessons/', views.LessonListView.as_view(), name='lesson_list'),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
]