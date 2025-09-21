from rest_framework import serializers
from .models import Question, Submission

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id","title","body","qtype","options","tags","created_at"]

    def validate(self, attrs):
        qtype = attrs.get("qtype", getattr(self.instance, "qtype", None))
        options = attrs.get("options", getattr(self.instance, "options", []))

        # MCQ: need at least 2 non-empty strings
        if qtype == "Multiple Choice":
            if not isinstance(options, list) or len(options) < 2 or not all(isinstance(x, str) and x.strip() for x in options):
                raise serializers.ValidationError({"options": "For MCQ, provide a list of >=2 non-empty strings.", "options values": options})

        # SCALE: default to 1..5 if not provided, and ensure min < max
        if qtype == "Scale":
            attrs["scale_min"] = 1
            attrs["scale_max"] = 5

        return attrs


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            "id","interview","question","answer_text",
            "metric_score","is_anonymous","consent_given","meta","submitted_at"
        ]
