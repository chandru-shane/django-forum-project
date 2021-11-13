from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                            related_name='profile',
                            on_delete=models.CASCADE)
    display_name = models.CharField(max_length=128)
    image = models.ImageField(default='profile_pics/default.png',upload_to='profile_pics')
    bio = models.CharField(max_length=256, blank=True, null=True)
    following = models.ManyToManyField(User, through='FollowingRelation')
    is_verified = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    blocked = models.ManyToManyField(User,related_name='blocked_by')
    created_at = models.DateTimeField(auto_now_add=True)
    udpated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return f"{self.user.username} Profile"
    
   
class FollowingRelation(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='followings')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.userprofile.display_name} | {self.user.username}"

    class Meta:
        unique_together = ("userprofile", "user")