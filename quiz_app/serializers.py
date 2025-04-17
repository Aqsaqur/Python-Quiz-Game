from rest_framework import serializers
from .models import Quiz, Question, Answer

class AnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializers(serializers.ModelSerializer):
    answers = AnswerSerializers(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'answers']  # Use actual field name from Question model

class QuizSerializers(serializers.ModelSerializer):
    questions = QuestionSerializers(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'questions']  # Use actual field names from Quiz model