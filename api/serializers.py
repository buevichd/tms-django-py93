from rest_framework import serializers

from polls.models import Question, Choice
from shop.models import Product, Category, Order, OrderEntry


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        include_products = self.context['request'].query_params.get('include_products', 'true')
        if include_products == 'false' and 'products' in self.fields:
            self.fields.pop('products')
        return super().to_representation(obj)

    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class OrderEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderEntry
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_entries = OrderEntrySerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class UpdateOrderEntrySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    remove = serializers.BooleanField(required=False, default=False)
    count = serializers.IntegerField(required=False, default=None, allow_null=True)


class UpdateOrderSerializer(serializers.Serializer):
    clear = serializers.BooleanField(required=False, default=False)
    order_entries = UpdateOrderEntrySerializer(many=True, required=False, default=[])
