import pytest
from django.urls import reverse

from testing.factories.quiz import QuestionFactory

QUESTION_1 = """
1) Which Python package would you like to learn more about?

- pandas
- numpy
- flask
- matplotlib
"""


@pytest.mark.django_db
class TestQuestionList:

    def setup(self):
        self.url = reverse('api:question-list')

    def test_create_question(self, api_client):
        data = {'body': QUESTION_1}
        response = api_client.post(self.url, data=data)
        assert response.status_code == 201

    def test_invalid_question_returns_error(self, api_client):
        data = {'body': 'foobar'}
        response = api_client.post(self.url, data=data)
        assert response.status_code == 400


@pytest.mark.django_db
class TestQuestionDetail:

    def get_url(self, question_instance):
        return reverse(
            'api:question-detail',
            kwargs={'uuid': question_instance.uuid.hex}
        )

    def test_retrieve(self, api_client):
        question_instance = QuestionFactory.create(text='text')
        url = self.get_url(question_instance)
        data = {'uuid': question_instance.uuid.hex}
        response = api_client.get(url, data=data)

        assert response.status_code == 200

    def test_destroy(self, api_client):
        question_instance = QuestionFactory.create(text='text')
        url = self.get_url(question_instance)
        data = {'uuid': question_instance.uuid.hex}
        response = api_client.delete(url, data=data)

        assert response.status_code == 204

    def test_question_cannot_be_updated(self, api_client):
        question_instance = QuestionFactory.create(text='text')
        url = self.get_url(question_instance)
        data = {'uuid': question_instance.uuid.hex, 'text': 'foo'}

        with pytest.raises(NotImplementedError):
            api_client.put(url, data=data)
