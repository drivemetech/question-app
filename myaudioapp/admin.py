from django.contrib import admin
from .models import Answer, Question, Notification, Category, Like

# Register your models here.

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Notification)
admin.site.register(Category)
admin.site.register(Like)