from rest_framework import serializers
from .models import Question, Submission

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id","title","body","qtype","tags","created_at"]

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            "id","interview","question","answer_text",
            "metric_score","is_anonymous","consent_given","meta","submitted_at"
        ]
