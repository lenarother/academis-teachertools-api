import pytest

from testing.factories import quiz


@pytest.mark.django_db
def test_question_has_meaningful_representation():
    question = quiz.QuestionFactory(body='How many apples do you have?')
    assert f'{question}' == 'How many apples do y...'


@pytest.mark.django_db
def test_answer_has_meaningful_representation():
    answer = quiz.AnswerFactory(text='pandas')
    assert f'{answer}' == 'pandas'
