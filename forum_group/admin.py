from django.contrib import admin

from . import models

# Register your models here.


admin.site.register(models.ForumGroup)
admin.site.register(models.ForumGroupRelation)
admin.site.register(models.JoinRequest)
