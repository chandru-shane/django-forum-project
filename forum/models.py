from django.db import models
from django.contrib.auth import get_user_model
from forum_group.models import ForumGroup

# Create your models here.

User = get_user_model()

class PostManager(models.Manager):
    def feed(self, user):
        posts = []
        membered_groups = user.group_members.all()
        for group in membered_groups:
            posts += group.posts.all()
        posts = sorted(posts, key=lambda post: post.created_on, reverse=True)
        return posts

class Post(models.Model):
    group = models.ForeignKey('forum_group.ForumGroup', on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(max_length=128)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')
    content = models.TextField(null=True, blank=True)
    upvote = models.ManyToManyField(User, through='PostUpVoteRelation', related_name='post_upvote_relation')
    downvote = models.ManyToManyField(User, through='PostDownVoteRelation', related_name='post_downvote_relation')
    upvote_count = models.IntegerField(default=0)
    downvote_count = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    objects = PostManager()
    
    def __str__(self):
        return f"{self.title} {self.content}"


class Comment(models.Model):
    body = models.TextField()
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_by_user')
    upvote = models.ManyToManyField(User, through='CommentUpVoteRelation', related_name='comment_upvote_relations')
    downvote = models.ManyToManyField(User, through='CommentDownVoteRelation', related_name='comment_down_relations')
    upvote_count = models.IntegerField(default=0)
    downvote_count = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.body}"


class CommentMapper(models.Model):
    post = models.ForeignKey('forum.post', on_delete=models.CASCADE, null=True, blank=True,related_name='post_comment')
    comment = models.ForeignKey('forum.Comment', on_delete=models.CASCADE,null=True, blank=True, related_name='comment_comment')
    reply_comment = models.ForeignKey('forum.Comment', on_delete=models.CASCADE, related_name='reply_comment')

    def __str__(self):
        if self.post is not None:
            return f"POST: {self.post.title} {self.reply_comment.body}"
        else:
            return f"COMMENT: {self.comment.body} {self.reply_comment.body}"


class PostUpVoteRelation(models.Model):
    post = models.ForeignKey('forum.Post', on_delete=models.CASCADE, related_name='post_upvotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user_upvotes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Upvote {self.post.title} {self.user.username}"

    class Meta:
        unique_together = ("post", "user")


class PostDownVoteRelation(models.Model):
    post = models.ForeignKey('forum.Post', on_delete=models.CASCADE, related_name='post_downvotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user_downvotes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DownVote {self.post.title} {self.user.username}"
    
    class Meta:
        unique_together = ("post", "user")


class CommentUpVoteRelation(models.Model):
    comment = models.ForeignKey('forum.Comment', on_delete=models.CASCADE,  related_name='comment_upvotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user_upvotes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Upvote {self.comment.body} {self.user.username}"

    class Meta:
        unique_together = ("comment", "user")


class CommentDownVoteRelation(models.Model):
    comment = models.ForeignKey('forum.Comment', on_delete=models.CASCADE, related_name='comment_downvotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user_downvotes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DownVote {self.comment.body} {self.user.username}"
    
    class Meta:
        unique_together = ("comment", "user")
