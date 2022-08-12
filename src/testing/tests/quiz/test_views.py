import pytest
from django.urls import reverse

from testing.factories.quiz import AnswerFactory, QuestionFactory
from testing.resources.testdata import questions


@pytest.mark.django_db
class TestQuestionList:

    def setup(self):
        self.url = reverse('api:question-list')

    def test_create_question(self, api_client):
        data = {'body': questions.Q1}
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


class TestQuestionPreview:

    def setup(self):
        self.url = reverse('api:question-preview')

    def test_preview_question_without_saving(self, api_client):
        data = {'body': questions.Q1}
        response = api_client.post(self.url, data=data)
        assert response.status_code == 200

    def test_invalid_question_cannot_be_previued(self, api_client):
        data = {'body': 'foo'}
        response = api_client.post(self.url, data=data)
        assert response.status_code == 400


@pytest.mark.django_db
class TestVote:

    def get_url(self, question_instance):
        return reverse(
            'api:question-vote',
            kwargs={'uuid': question_instance.uuid.hex}
        )

    def test_answer_can_be_voted_on(self, api_client):
        answer_instance = AnswerFactory.create()
        assert answer_instance.votes == 0

        url = self.get_url(answer_instance.question)
        data = {'answer_uuid': answer_instance.uuid.hex}
        response = api_client.post(url, data=data)
        answer_instance.refresh_from_db()
        assert response.status_code == 201
        assert answer_instance.votes == 1


@pytest.mark.django_db
class TestQuestionResult:

    def get_url(self, question_instance):
        return reverse(
            'api:question-result',
            kwargs={'uuid': question_instance.uuid.hex}
        )

    def test_get_question_votes_for_chart(self, api_client):
        question = QuestionFactory.create()
        answer_1 = AnswerFactory.create(question=question, votes=2)
        answer_2 = AnswerFactory.create(question=question, votes=0)
        answer_3 = AnswerFactory.create(question=question, votes=1)

        url = self.get_url(question)
        response = api_client.get(url,)
        assert response.status_code == 200
        assert response.json() == {
            'name': 'Answers',
            'colorByPoint': True,
            'data': [
                {
                    'name': answer_1.text,
                    'y': answer_1.votes,
                },
                {
                    'name': answer_2.text,
                    'y': answer_2.votes,
                },
                {
                    'name': answer_3.text,
                    'y': answer_3.votes,
                },

            ]

        }
