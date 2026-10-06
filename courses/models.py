from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Max
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date_start = models.DateField()
    date_end = models.DateField()

    tags = models.ManyToManyField(
        Tag,
        related_name='courses',
        blank=True,
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses',
    )

    class Meta:
        ordering = ['-date_start']

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(editable=False)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
    )

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=['course', 'order'],
                name='unique_lesson_order_per_course'
            )
        ]

    def save(self, *args, **kwargs):
        if self._state.adding:
            with transaction.atomic():
                Course.objects.select_for_update().get(pk=self.course_id)

                max_order = Lesson.objects.filter(course=self.course).aggregate(
                    Max('order')
                )['order__max']
                self.order = (max_order or 0) + 1
                return super().save(*args, **kwargs)

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.title} - Урок {self.order}: {self.title}"