from django.urls import path

from teachertools.quiz import views

urlpatterns = [
    path(
        'preview/',
        views.QuestionPreview.as_view(),
        name='question-preview'
    ),
    path(
        '<str:uuid>/',
        views.QuestionDetail.as_view(),
        name='question-detail'
    ),
    path(
        '',
        views.QuestionList.as_view(),
        name='question-list'
    ),
]
