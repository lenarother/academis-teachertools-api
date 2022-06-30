from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from teachertools.quiz.models import Question
from teachertools.quiz.serializers import (
    QuestionPreviewSerializer,
    QuestionSerializer
)


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

    @csrf_exempt
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
