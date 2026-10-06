from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Course, Lesson, Tag
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CourseSerializer,
    LessonCreateUpdateSerializer,
    LessonSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    search_fields = ['name', 'slug']
    ordering = ['name']


class CourseViewSet(viewsets.ModelViewSet):
    queryset = (
        Course.objects.select_related('owner')
        .prefetch_related('tags')
        .all()
    )
    serializer_class = CourseSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    filterset_fields = ['tags', 'owner']
    search_fields = ['title', 'description', 'tags__name']
    ordering_fields = ['price', 'date_start', 'id']
    ordering = ['id']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def free(self, request):
        free_courses = self.get_queryset().filter(price=0)

        page = self.paginate_queryset(free_courses)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(free_courses, many=True)
        return Response(serializer.data)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.select_related('course', 'course__owner').all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    filterset_fields = ['course', 'order']
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'id']
    ordering = ['course', 'order']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return LessonCreateUpdateSerializer
        return LessonSerializer