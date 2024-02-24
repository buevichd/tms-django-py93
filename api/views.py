from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from rest_framework import status
from rest_framework import viewsets, filters, views
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import QuestionSerializer, ChoiceSerializer, ProductSerializer, \
    CategorySerializer, OrderSerializer, UpdateOrderSerializer
from polls.models import Question, Choice
from shop.models import Product, Category, Order
from .filters import ChoiceCountFilter, CategoryIdFilter


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


class ProductViewSet(viewsets.mixins.RetrieveModelMixin,
                     viewsets.mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    filter_backends = [CategoryIdFilter]


class CategoryViewSet(viewsets.mixins.RetrieveModelMixin,
                      viewsets.mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer


class AddToCartView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        product = get_object_or_404(Product, id=product_id)
        request.user.profile.shopping_cart.add_product(product)
        return Response(status=status.HTTP_200_OK)


class CartView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        return Response(OrderSerializer(request.user.profile.shopping_cart).data)


class UpdateCartView(views.APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request: Request):
        update_order = UpdateOrderSerializer(data=request.data)
        update_order.is_valid(raise_exception=True)

        order: Order = request.user.profile.shopping_cart
        update_order_data: dict = update_order.validated_data
        self._update_order(order, update_order_data)
        return Response(OrderSerializer(order).data)

    def _update_order(self, order: Order, update_order_data: dict):
        if update_order_data['clear']:
            order.order_entries.all().delete()
        else:
            for update_order_entry_data in update_order_data['order_entries']:
                self._update_order_entry(order, update_order_entry_data)

    def _update_order_entry(self, order: Order, update_order_entry_data: dict):
        order_entry_id = update_order_entry_data['id']
        order_entry = order.order_entries.filter(id=order_entry_id).first()
        if order_entry is None:
            raise ValidationError(f'Unknown order entry id {order_entry_id}')
        if update_order_entry_data['remove']:
            order_entry.delete()
        elif update_order_entry_data['count'] is not None:
            order_entry.count = update_order_entry_data['count']
            order_entry.save()
