from rest_framework import generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer, LessonCreateUpdateSerializer


class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListView(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Lesson.objects.all()
        course_id = self.request.query_params.get('course')
        order = self.request.query_params.get('order')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if order:
            queryset = queryset.filter(order=order)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LessonCreateUpdateSerializer
        return LessonSerializer


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return LessonCreateUpdateSerializer
        return LessonSerializer