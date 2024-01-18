from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Product, Category, Profile, OrderEntry, Order

admin.site.register(Product)


class ProductInline(admin.StackedInline):
    model = Product
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]


admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0


@admin.register(User)
class ShopUserAdmin(UserAdmin):
    inlines = [ProfileInline]


admin.site.register(OrderEntry)


class OrderEntryInline(admin.TabularInline):
    model = OrderEntry
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderEntryInline]
