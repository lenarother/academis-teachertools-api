from django.urls import path

from teachertools.quiz import views

urlpatterns = [
    path('', views.QuestionList.as_view(), name='question-list'),
]
