from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from notes.models import Note
from rest_framework.test import APITestCase


class NotePermissionsTest(APITestCase):
    def setUp(self):
        # create 2 users
        self.user1 = User.objects.create_user(username="Debo", password="pass1234")
        self.user2 = User.objects.create_user(username="Adura", password="pass1234")
        # create notes for users
        Note.objects.create(
            title="Note by Debo",
            content="Content for Debo's note",
            owner=self.user1,
        )
        Note.objects.create(
            title="Note by Adura",
            content="Content for Adura's note",
            owner=self.user2,
        )
        # authenticate Debo with jwt
        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_user_sees_only_own_notes(self):
        response = self.client.get("/api/v1/notes/")
        self.assertEqual(response.status_code, 200)
        results = response.data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Note by Debo")
