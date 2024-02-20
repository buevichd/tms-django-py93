from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.request import Request

from api.serializers import QuestionSerializer, ChoiceSerializer
from polls.models import Question, Choice
from .filters import ChoiceCountFilter


def get_active_questions():
    return Question.objects \
        .annotate(choice_count=Count('choices')) \
        .filter(status=Question.Status.APPROVED,
                pub_date__lte=timezone.now(),
                choice_count__gte=2) \
        .order_by('-pub_date')


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = get_active_questions().prefetch_related('choices')
    serializer_class = QuestionSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter,
                       ChoiceCountFilter]
    ordering_fields = ['question_text', 'pub_date']
    search_fields = ['question_text']


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['choice_text']
    search_fields = ['choice_text', 'question__question_text']


@api_view(['POST'])
def choice_vote(request: Request, question_id: int):
    question = get_object_or_404(get_active_questions(), id=question_id)
    selected_choice = get_object_or_404(question.choices, id=request.data['choice'])
    selected_choice.votes += 1
    selected_choice.save()
    return redirect('question-detail', question_id)
