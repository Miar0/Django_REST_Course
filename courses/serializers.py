from rest_framework import serializers
from .models import Tag, Course, Lesson


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class CourseSerializer(serializers.ModelSerializer):
    duration_days = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.username')

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
            'tags',
            'owner',
        ]

    def get_duration_days(self, obj):
        return (obj.date_end - obj.date_start).days

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Price cannot be negative.')
        return value

    def validate(self, data):
        date_start = data.get('date_start')
        date_end = data.get('date_end')

        if self.instance:
            date_start = date_start or self.instance.date_start
            date_end = date_end or self.instance.date_end

        if date_start and date_end and date_end < date_start:
            raise serializers.ValidationError(
                'End date cannot be earlier than start date.'
            )
        return data


class LessonSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'description',
            'order',
            'course',
            'course_title',
        ]


class LessonCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'description',
            'order',
            'course',
        ]
        read_only_fields = ['order']

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                'Lesson title must be at least 3 characters long.'
            )
        return value