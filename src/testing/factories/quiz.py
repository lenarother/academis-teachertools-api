import factory

from teachertools.quiz.models import Question


class QuestionFactory(factory.django.DjangoModelFactory):
    body = factory.Faker('sentence')

    class Meta:
        model = Question
