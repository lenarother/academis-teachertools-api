from django.contrib import admin

from .models import Answer, Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'created', 'text')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'text')
