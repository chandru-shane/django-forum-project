from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from profiles.models import UserProfile


def create_user(username='testuser00', email='test@gmail.com',password='passfortest'):
    User = get_user_model()
    testuser = User.objects.create_user(username=username,email=email, password=password)
    return testuser


class TestUserProfileModel(TestCase):
    """
    Test is to test UserProfile model
    """


    def setUp(self):
        self.User = get_user_model()
    
    def test_create_userprofile(self):
        """
        Test the user profile creatation
        """
        user = create_user()
        user_profile = UserProfile.objects.get(user=user)
        
        self.assertEqual(user_profile.display_name, user.username)
    
    def test_create_userprofile_inner_test(self):
        """
        Test that display name  not after updated username
         """
        user = create_user()
        created_user = self.User.objects.get(username=user.username)
        created_user.username='newgoal'
        created_user.save()
        new_username = self.User.objects.get(username='newgoal')
        self.assertEqual(new_username.email, created_user.email)
        user_profile = UserProfile.objects.get(user=created_user)
        self.assertNotEqual(new_username.username,
                            user_profile.display_name)
        self.assertEqual('testuser00', user_profile.display_name)