from datetime import date, timedelta
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Course


class CoursePermissionsAndValidationTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='password123')
        self.other_user = User.objects.create_user(username='other', password='password123')

        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            price=100.00,
            date_start=date.today(),
            date_end=date.today() + timedelta(days=30),
            owner=self.owner,
        )
        self.url = f'/api/courses/{self.course.pk}/'

    def test_anyone_can_read(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_edit(self):
        response = self.client.patch(self.url, {'price': '50.00'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_user_cannot_edit(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(self.url, {'price': '50.00'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_edit(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.url, {'price': '50.00'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(float(self.course.price), 50.00)

    def test_validate_negative_price(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.url, {'price': '-10.00'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)

    def test_validate_dates(self):
        self.client.force_authenticate(user=self.owner)
        invalid_end_date = self.course.date_start - timedelta(days=1)
        response = self.client.patch(self.url, {'date_end': invalid_end_date})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)