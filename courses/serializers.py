from rest_framework import serializers
from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    duration_days = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'price',
            'date_start',
            'date_end',
            'duration_days',
        ]

    def get_duration_days(self, obj):
        return (obj.date_end - obj.date_start).days


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()

    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'description',
            'order',
            'course',
        ]


class LessonCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'description',
            'order',
            'course'
        ]
        read_only_fields = ['order']
