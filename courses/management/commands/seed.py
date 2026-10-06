from datetime import date, timedelta
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from courses.models import Course, Lesson, Tag


class Command(BaseCommand):
    help = 'Seed database with sample courses, tags, and lessons'

    def handle(self, *args, **options):
        if Course.objects.exists():
            self.stdout.write(self.style.WARNING('Data already exists, skipping.'))
            return

        admin_user, _ = User.objects.get_or_create(username='admin', is_staff=True, is_superuser=True)
        admin_user.set_password('admin')
        admin_user.save()

        author, _ = User.objects.get_or_create(username='danko')
        author.set_password('danko228')
        author.save()

        tag_backend = Tag.objects.create(name='Backend', slug='backend')
        tag_python = Tag.objects.create(name='Python', slug='python')
        tag_api = Tag.objects.create(name='REST API', slug='rest-api')

        course_paid = Course.objects.create(
            title='Python Backend Intensive',
            description='Comprehensive course on Django and FastAPI.',
            price=150.00,
            date_start=date.today(),
            date_end=date.today() + timedelta(days=60),
            owner=author,
        )
        course_paid.tags.set([tag_backend, tag_python])

        course_free = Course.objects.create(
            title='Introduction to Web APIs',
            description='Free introductory tutorial on REST fundamentals.',
            price=0.00,
            date_start=date.today() + timedelta(days=5),
            date_end=date.today() + timedelta(days=20),
            owner=admin_user,
        )
        course_free.tags.set([tag_api])

        Lesson.objects.create(
            title='HTTP & REST Basics',
            description='Learn verbs, headers, and status codes.',
            course=course_free,
        )
        Lesson.objects.create(
            title='Advanced ORM and Indexing',
            description='Optimizing queries with select_related and prefetch_related.',
            course=course_paid,
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded sample data.'))