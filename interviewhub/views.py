from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, serializers
from .models import Question, Submission, Interview
from .serializers import QuestionSerializer, SubmissionSerializer, InterviewSerializer
from django.db import IntegrityError
from django.db.models import Q


class WhoAmIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        u = request.user
        return Response({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "is_staff": u.is_staff,
        })

class QuestionListCreateView(generics.ListCreateAPIView):
    # GET: list questions
    # POST: create a question

    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Override get_queryset to have the results ordered by creation date and allow filters (question type, tag or search)
    def get_queryset(self):
        qs = Question.objects.all().order_by("-created_at")

        qtype = self.request.query_params.get("qtype")
        if qtype:
            qs = qs.filter(qtype=qtype)

        tag = self.request.query_params.get("tag")
        if tag:
            qs = qs.filter(tags__icontains=tag)

        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(body__icontains=search))

        return qs

class QuestionDetailView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.AllowAny]

class SubmissionListView(generics.ListAPIView):
    # GET: list the user's submissions
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Override get_queryset to have the results ordered by submission date
    def get_queryset(self):
        return Submission.objects.filter(candidate=self.request.user).order_by("-submitted_at")

class SubmissionCreateView(generics.CreateAPIView):
    # POST: create a submission
    # Body must include: interview (id), question (id), answer_text
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Set the candidate as the logged-in user
        try:
            serializer.save(candidate=self.request.user)
        except IntegrityError:
            # No unique_together (candidate, interview, question)
            raise serializers.ValidationError(
                {"non_field_errors": ["You have already answered this question for this interview."]}
            )

class InterviewListCreateView(generics.ListCreateAPIView):
    # GET: list interviews
    # POST: create an interview
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Override get_queryset to have the results ordered by creation date
    def get_queryset(self):
        # Show all interviews
        return Interview.objects.all().order_by("-created_at")

    def perform_create(self, serializer):
        # Owner = current user
        serializer.save(owner=self.request.user)

class InterviewDetailView(generics.RetrieveAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    permission_classes = [permissions.AllowAny]
