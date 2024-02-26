from django.contrib import admin
from media.models import UserProfile,Post,Like,Connection
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Connection)
admin.site.register(Post)
admin.site.register(Like)