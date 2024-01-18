from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class OrderEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='+')
    count = models.IntegerField(default=0)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_entries')

    def __str__(self):
        return f'{self.product} - {self.count}'


class OrderStatus(models.TextChoices):
    INITIAL = "IN", _("Initial")
    COMPLETED = "CO", _("Completed")
    DELIVERED = "DE", _("Delivered")


class Order(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=2, choices=OrderStatus.choices,
                              default=OrderStatus.INITIAL)

    def __str__(self):
        return f'id:{self.id} - {self.profile} - {self.status}'

    def add_product(self, product: Product):
        order_entry: OrderEntry = self.order_entries.filter(product=product).first()
        if not order_entry:
            order_entry = self.order_entries.create(product=product, count=0)
        order_entry.count += 1
        order_entry.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL,
                                null=True, blank=True, default=None)
    shopping_cart = models.OneToOneField(Order, on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='+')

    def __str__(self):
        return str(self.user)

