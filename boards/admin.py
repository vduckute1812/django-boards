from django.contrib import admin

# Register your models here.
from boards.models import Board, Topic, User, Post

admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)

# admin.site.register(User)