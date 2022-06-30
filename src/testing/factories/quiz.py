import factory

from teachertools.quiz.models import Answer, Question


class QuestionFactory(factory.django.DjangoModelFactory):
    body = factory.Faker('sentence')

    class Meta:
        model = Question


class AnswerFactory(factory.django.DjangoModelFactory):
    text = factory.Faker('sentence')
    question = factory.SubFactory(QuestionFactory)

    class Meta:
        model = Answer
