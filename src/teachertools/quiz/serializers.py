import uuid

from rest_framework import serializers

from teachertools.markdown_edit.services import (is_question_valid,
                                                 parse_question)
from teachertools.quiz.models import Answer, Question


class ReadOnlyModelSerializer(serializers.ModelSerializer):

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        for field in fields:
            fields[field].read_only = True
        return fields


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


class VoteSerializer(serializers.Serializer):
    answer_uuid = serializers.UUIDField(format='hex', required=True)

    def validate(self, attrs):
        question_uuid = self.context.get('question_uuid')
        answer_uuid = attrs['answer_uuid']
        answer_instance = Answer.objects.get(uuid=answer_uuid)

        if not answer_instance.question.uuid.hex == question_uuid:
            raise serializers.ValidationError('No such answer')

        return attrs

    def create(self, validated_data):
        answer_instance = Answer.objects.get(
            uuid=validated_data.get('answer_uuid')
        )
        answer_instance.votes += 1
        answer_instance.save()
        return answer_instance


class AnswerResultSerializer(ReadOnlyModelSerializer):
    name = serializers.CharField(source='text')
    y = serializers.IntegerField(source='votes')

    class Meta:
        model = Answer
        fields = ['name', 'y']


class QuestionResultSerilaizer(ReadOnlyModelSerializer):
    data = AnswerResultSerializer(many=True, source='answers')

    class Meta:
        model = Question
        fields = ['data']
