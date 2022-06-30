import uuid
from unittest import mock

import pytest
from freezegun import freeze_time

from teachertools.quiz.models import Question
from teachertools.quiz.serializers import QuestionSerializer
from testing.factories.quiz import AnswerFactory, QuestionFactory
from testing.resources.testdata import questions


@pytest.mark.django_db
def test_question_is_saved_correctly():
    data = {'body': questions.Q1}
    question_serializer = QuestionSerializer(data=data)
    assert question_serializer.is_valid() is True

    dt_now = '2012-01-14 03:21'
    with freeze_time(dt_now):
        question = question_serializer.save()

    assert isinstance(question, Question)
    assert question.body == questions.Q1.strip()
    assert question.text == questions.Q1_TEXT
    assert question.answers.count() == 4
    assert isinstance(question.uuid, uuid.UUID)
    assert f'{question.created:%Y-%m-%d %H:%M}' == dt_now


@pytest.mark.django_db
def test_question_instance_is_correctly_serialized():
    question_instance = QuestionFactory.create(text='text')
    answer_instance = AnswerFactory.create(
        question=question_instance,
        text='answer text',
    )
    AnswerFactory.create(text='not related answer text')
    serializer = QuestionSerializer(question_instance)

    assert serializer.data == {
        'text': 'text',
        'uuid': question_instance.uuid.hex,
        'answers': [
            {
                'text': 'answer text',
                'uuid': answer_instance.uuid.hex,
            },
        ],
        'body': mock.ANY,
    }


def test_cannot_create_invalid_question():
    data = {'body': 'foo bar'}
    question_serializer = QuestionSerializer(data=data)
    assert question_serializer.is_valid() is False
    assert 'body' in question_serializer.errors
