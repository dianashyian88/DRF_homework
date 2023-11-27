from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User
from education.models import Lesson, Subscription, Course


class EducationTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(username='Тестов Тест Тестович', email='test3@mail.ru', password='123456qwerty')
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """Тестирование создания урока"""

        data = {
            "name": "Урок 13. DRF",
            "link_to_video": "http://youtube.com/check?uri=",
            "description": "В этом урок вы изучите DRF"
        }
        response = self.client.post(
            '/lesson/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "name": "Урок 13. DRF",
                "image": None,
                "description": "В этом урок вы изучите DRF",
                "link_to_video": "http://youtube.com/check?uri=",
                "course": None,
                "owner": 1
            }
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_list_lesson(self):
        """Тестирование выведения списка уроков"""

        Lesson.objects.create(
            id=1,
            name="Урок 13. DRF",
            link_to_video="http://youtube.com/check?uri=",
            description="В этом урок вы изучите DRF",
            owner=self.user
        )

        response = self.client.get(
            '/lesson/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results':
                [
                    {
                    "id": 1,
                    "name": "Урок 13. DRF",
                    "image": None,
                    "description": "В этом урок вы изучите DRF",
                    "link_to_video": "http://youtube.com/check?uri=",
                    "course": None,
                    "owner": 5
                    }
                ]
             }
        )

    def test_retrieve_lesson(self):
        """Тестирование выведения информации об уроке"""

        Lesson.objects.create(
            id=1,
            name="Урок 13. DRF",
            link_to_video="http://youtube.com/check?uri=",
            description="В этом урок вы изучите DRF",
            owner=self.user
        )

        response = self.client.get(
            '/lesson/1/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "name": "Урок 13. DRF",
                "image": None,
                "description": "В этом урок вы изучите DRF",
                "link_to_video": "http://youtube.com/check?uri=",
                "course": None,
                "owner": 6
            }
        )

    def test_update_lesson(self):
        """Тестирование обновления информации об уроке"""

        Lesson.objects.create(
            id=1,
            name="Урок 13. DRF",
            link_to_video="http://youtube.com/check?uri=",
            description="В этом урок вы изучите DRF",
            owner=self.user
        )

        data = {
            "name": "Урок 13. DRF PRO",
            "link_to_video": "http://youtube.com/check?uri=ert",
            "description": "В этом урок вы изучите DRF на более углубленном уровне"
        }

        response = self.client.put(
            '/lesson/update/1/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "name": "Урок 13. DRF PRO",
                "image": None,
                "description": "В этом урок вы изучите DRF на более углубленном уровне",
                "link_to_video": "http://youtube.com/check?uri=ert",
                "course": None,
                "owner": 7
            }
        )

    def test_destroy_lesson(self):
        """Тестирование удаления урока"""

        Lesson.objects.create(
            id=1,
            name="Урок 13. DRF",
            link_to_video="http://youtube.com/check?uri=",
            description="В этом урок вы изучите DRF",
            owner=self.user
        )

        response = self.client.delete(
            '/lesson/delete/1/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_create_subscription(self):
        """Тестирование создания подписки"""

        Course.objects.create(
            id=1,
            name="Основы SQL",
            description="В этом курсе вы изучите основы SQL",
            owner=self.user
        )

        data = {
            "course": 1,
            "student": self.user.pk,
            "is_active": True
        }
        response = self.client.post(
            '/subscription/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "course": 1,
                "is_active": True,
                "student": 2
            }
        )

        self.assertTrue(
            Subscription.objects.all().exists()
        )

    def test_destroy_subscription(self):
        """Тестирование удаления подписки"""

        Course.objects.create(
            id=1,
            name="Основы SQL",
            description="В этом курсе вы изучите основы SQL",
            owner=self.user
        )

        data = {
            "course": 1,
            "student": self.user.pk,
            "is_active": True
        }

        self.client.post(
            '/subscription/create/',
            data=data
        )

        response = self.client.delete(
            '/subscription/delete/2/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
