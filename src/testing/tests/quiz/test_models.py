import pytest

from testing.factories.quiz import QuestionFactory


@pytest.mark.django_db
def test_question_has_meaningful_representation():
    question = QuestionFactory(body='How many apples do you have?')
    assert f'{question}' == 'How many apples do y...'
