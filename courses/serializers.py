from rest_framework import serializers
from .models import Question, Answer, Lecture, Content


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('question', 'answer', 'correct')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'title', 'data_field', 'answers')


class ContentSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(source="content_type.name")
    class Meta:
        model = Content
        fields = ('id', 'content_type', 'object_id', 'lecture')


class LectureSerializer(serializers.HyperlinkedModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Lecture
        fields = ('title', 'order', 'contents')
