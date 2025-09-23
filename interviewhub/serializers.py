from rest_framework import serializers
from .models import Question, Submission, Interview


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            "id",
            "interview",
            "question",
            "answer_text",
            "is_anonymous",
            "consent_given",
            "meta",
            "metric_score",
            "submitted_at",
        ]
        read_only_fields = ["metric_score", "submitted_at"]

    def validate(self, attrs):
        interview = attrs.get("interview")
        question = attrs.get("question")
        answer_text = attrs.get("answer_text", "")

        # Check if Question belong to Interview
        if interview and question:
            if not interview.questions.filter(pk=question.pk).exists():
                raise serializers.ValidationError({"question": "This question is not part of the selected interview."})

        if question:
            if question.qtype == Question.MULTIPLE_CHOICE:
                # Accept either the answer text of the option or the index
                if not question.options:
                    raise serializers.ValidationError({"answer_text": "Multiple Choice requires 'options' on the question."})
                valid = False
                if answer_text in question.options:
                    valid = True
                else:
                    try:
                        idx = int(answer_text)
                        if 0 <= idx < len(question.options):
                            valid = True
                    except (ValueError, TypeError):
                        pass
                if not valid:
                    raise serializers.ValidationError(
                        {"answer_text": "For Multiple Choice, provide either the option text or a zero-based index of the option."}
                    )

            elif question.qtype == Question.SCALE:
                # Accept only int between 1 and 5 as answer
                try:
                    val = int(answer_text)
                except (ValueError, TypeError):
                    raise serializers.ValidationError({"answer_text": "For SCALE, answer_text must be an integer."})
                lo = 1
                hi = 5
                if not (lo <= val <= hi):
                    raise serializers.ValidationError(
                        {"answer_text": f"Scale answer must be between {lo} and {hi}."}
                    )

        return attrs

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id",
            "title",
            "body",
            "qtype",
            "options",
            "tags",
            "created_at"
        ]

    def validate(self, attrs):
        qtype = attrs.get("qtype", getattr(self.instance, "qtype", None))
        options = attrs.get("options", getattr(self.instance, "options", []))

        # Check if Multiple Choice have at least 2 strings as options
        if qtype == "Multiple Choice":
            if not isinstance(options, list) or len(options) < 2 or not all(isinstance(x, str) and x.strip() for x in options):
                raise serializers.ValidationError({"options": "For Multiple Choice, provide a list of >=2 non-empty strings.", "options values": options})

        return attrs

class InterviewSerializer(serializers.ModelSerializer):
    # On write validates each Question ID exists and gives list of Questions
    # On read shows questions as a list of IDs
    questions = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), many=True, required=False)

    # On read only gives an array of questions existent in the Interview
    questions_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Interview
        fields = [
            "id",
            "title",
            "description",
            "is_published",
            "scheduled_at",
            "questions",
            "questions_data",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    # Called on read to build the list from obj.questions.all()
    def get_questions_data(self, obj):
        return [
            {
                "id": q.id,
                "title": q.title,
                "qtype": q.qtype,
                "tags": q.tags,
            }
            for q in obj.questions.all()
        ]

    def create(self, validated_data):
        # Gets list of Question instances from validated_data
        questions = validated_data.pop("questions", [])
        # Create the Interview row on DB
        interview = Interview.objects.create(**validated_data)
        if questions:
            # Writes the Many-to-Many join rows
            interview.questions.set(questions)
        return interview

    def update(self, instance, validated_data):
        questions = validated_data.pop("questions", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        if questions is not None:
            instance.questions.set(questions) # If questions provided, replace the M2M set with .set(questions)
        return instance
