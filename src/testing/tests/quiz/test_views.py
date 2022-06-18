import pytest
from django.urls import reverse

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
