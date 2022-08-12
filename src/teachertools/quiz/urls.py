from django.urls import path

from teachertools.quiz import views

urlpatterns = [
    path(
        'preview/',
        views.QuestionPreview.as_view(),
        name='question-preview'
    ),
    path(
        'vote/<str:uuid>/',
        views.QuestionVote.as_view(),
        name='question-vote'
    ),
    path(
        'result/<str:uuid>/',
        views.QuestionResult.as_view(),
        name='question-result'
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
