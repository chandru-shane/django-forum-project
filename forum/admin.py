from django.contrib import admin
from django.db.models.fields.related import RelatedField

from . import models

admin.site.register(models.Post)
admin.site.register(models.CommentMapper)
admin.site.register(models.Comment)
admin.site.register(models.PostUpVoteRelation)
admin.site.register(models.PostDownVoteRelation)
admin.site.register(models.CommentUpVoteRelation)
admin.site.register(models.CommentDownVoteRelation)
