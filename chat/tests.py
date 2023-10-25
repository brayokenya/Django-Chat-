from django.test import TestCase
from django.urls import reverse
from chat.models import Group, Message
from members.models import Members
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatAppTestCase(TestCase):
    def setUp(self):
        # Create a test user using the custom manager
        self.user = Members.objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )
        self.user.username = 'testuser'  # Set the username
        self.user.save()

    def test_user_signup(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'user_email': 'newuser@example.com',
            'user_pass': 'newpassword',
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertTrue(self.client.login(username='newuser@example.com', password='newpassword'))
        self.assertRedirects(response, reverse('home'))

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'user_email': 'testuser@example.com',
            'user_pass': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertRedirects(response, reverse('home'))

    def test_user_logout_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertRedirects(response, reverse('login'))

    def test_user_logout_unauthenticated(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertRedirects(response, reverse('login'))

    def test_add_and_remove_user_from_group(self):
        # Create a new group
        group = Group.objects.create()

        # Ensure the user is not initially in the group
        self.assertNotIn(self.user, group.members.all())

        # Add the user to the group
        group.add_user(self.user)

        # Check if the user is now in the group
        group.refresh_from_db()  # Refresh the group from the database
        self.assertIn(self.user, group.members.all())

        # Remove the user from the group
        group.remove_user(self.user)

        # Check if the user is no longer in the group
        group.refresh_from_db()  # Refresh the group from the database
        self.assertNotIn(self.user, group.members.all())

    def test_create_message(self):
        # Create a new group
        group = Group.objects.create()

        # Create a message for the group
        message = Message.objects.create(
            author=self.user,
            content='Hello, this is a test message.',
            group=group
        )

        # Retrieve the message from the database
        saved_message = Message.objects.get(pk=message.pk)

        # Check if the saved message attributes match the input
        self.assertEqual(saved_message.author, self.user)
        self.assertEqual(saved_message.content, 'Hello, this is a test message.')
        self.assertEqual(saved_message.group, group)
