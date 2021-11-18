from django.db import models

from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class ForumGroup(models.Model):
    name = models.CharField(max_length=255)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_user_groups')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(User, through='ForumGroupRelation', related_name='group_members')
    is_private = models.BooleanField(default=False)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_groups')


    def __str__(self):
        return f"{self.name} - {self.admin.username}"


class ForumGroupRelation(models.Model):
    group = models.ForeignKey('forum_group.ForumGroup',on_delete=models.CASCADE, related_name='group_relation')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_relation_member')

    class Meta:
        unique_together = "group", "user"

    def __str__(self):
        return f"{self.group.name} {self.user.username}"

class JoinRequest(models.Model):
    group = models.ForeignKey('forum_group.ForumGroup',on_delete=models.CASCADE, related_name='group_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='join_requests')

    class Meta:
        unique_together = "group", "user"

    def __str__(self):
        return f"{self.group.name} {self.user.username}"
