from django.db.models import QuerySet, Count
from rest_framework import filters
from rest_framework.request import Request


class ChoiceCountFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset: QuerySet, view):
        min_choice_count = request.query_params.get('min_choice_count')
        max_choice_count = request.query_params.get('max_choice_count')
        if min_choice_count is not None or max_choice_count is not None:
            queryset = queryset.annotate(choice_count=Count('choices'))
        if min_choice_count is not None:
            queryset = queryset.filter(choice_count__gte=min_choice_count)
        if max_choice_count is not None:
            queryset = queryset.filter(choice_count__lte=max_choice_count)
        return queryset


class CategoryIdFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset: QuerySet, view):
        category_id = request.query_params.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category__id=category_id)
        return queryset
