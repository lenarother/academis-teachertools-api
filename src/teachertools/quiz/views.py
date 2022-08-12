from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from teachertools.quiz.models import Question
from teachertools.quiz.serializers import (QuestionPreviewSerializer,
                                           QuestionResultSerilaizer,
                                           QuestionSerializer, VoteSerializer)


@method_decorator(csrf_exempt, name='dispatch')
class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


@method_decorator(csrf_exempt, name='dispatch')
class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'uuid'
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def put(self, request, *args, **kwargs):
        raise NotImplementedError


@method_decorator(csrf_exempt, name='dispatch')
class QuestionPreview(APIView):

    def post(self, request, format=None):
        serializer = QuestionPreviewSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@method_decorator(csrf_exempt, name='dispatch')
class QuestionVote(APIView):
    lookup_field = 'uuid'

    def get_object(self, uuid):
        try:
            return Question.objects.get(uuid=uuid)
        except Question.DoesNotExist:
            raise Http404

    def post(self, request, uuid):
        question = self.get_object(uuid)
        context = {'question_uuid': question.uuid.hex}
        serializer = VoteSerializer(data=request.data, context=context)

        if serializer.is_valid():
            serializer.save()

            return Response(
                # serializer.errors,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@method_decorator(csrf_exempt, name='dispatch')
class QuestionResult(APIView):
    lookup_field = 'uuid'

    def get_object(self, uuid):
        try:
            return Question.objects.get(uuid=uuid)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        question = self.get_object(uuid)
        serializer = QuestionResultSerilaizer(question)
        data = {
            'name': 'Answers',
            'colorByPoint': True,
            'data': serializer.data['data']
        }
        print(data)
        return Response(
            data,
            status=status.HTTP_200_OK
        )
