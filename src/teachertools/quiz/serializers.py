import uuid

from rest_framework import serializers

from teachertools.markdown_edit.services import (is_question_valid,
                                                 parse_question)
from teachertools.quiz.models import Answer, Question


class AnswerSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', default=uuid.uuid4)

    class Meta:
        model = Answer
        fields = ['uuid', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', default=uuid.uuid4)
    answers = AnswerSerializer(many=True, read_only=True)

    def validate_body(self, value):
        if not is_question_valid(value):
            raise serializers.ValidationError(
                'Question markdown invalid: no answers list detected.'
            )
        return value

    class Meta:
        model = Question
        fields = ['uuid', 'body', 'text', 'answers']

    def create(self, validated_data):
        text, answers = parse_question(validated_data.get('body', ''))
        question_instance = Question.objects.create(
            **validated_data,
            text=text
        )
        for answer in answers:
            Answer.objects.create(
                text=answer,
                question=question_instance
            )

        return question_instance


class QuestionPreviewSerializer(serializers.Serializer):
    body = serializers.CharField()

    def validate(self, attrs):
        body = attrs.get('body', '')
        if not is_question_valid(body):
            raise serializers.ValidationError(
                'Question markdown invalid: no answers list detected.'
            )
        return attrs

    def to_internal_value(self, data):
        body = data.get('body', '')
        if not is_question_valid(body):
            return data

        text, answers = parse_question(body)
        return {
            'uuid': '',
            'body': body,
            'text': text,
            'answers': [
                {'uuid': '', 'text': answer}
                for answer in answers
            ],
        }
