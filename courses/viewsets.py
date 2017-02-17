from rest_framework import viewsets, generics
from .models import Question, Lecture, Content
from .serializers import QuestionSerializer, LectureSerializer, ContentSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionList(generics.ListAPIView):
    #queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        ids = self.kwargs['ids'].split(',')
        return Question.objects.filter(id__in=ids)


class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

