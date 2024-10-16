from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ProductInfo, Product, ProductParameter, Parameter, Shop, Order, OrderItem, ConfirmEmailToken,\
    Contact, Category


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = (
        (None, {'fields': ('email', 'password', 'type')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'company', 'position')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'user', 'state']
    list_filter = ['name', 'url', 'user', 'state']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'dt', 'state', 'contact']
    list_filter = ['user', 'dt', 'state', 'contact']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_info', 'quantity']
    list_filter = ['order', 'product_info', 'quantity']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ['model', 'product', 'shop', 'quantity', 'price', 'rrc_price']
    list_filter = ['model', 'product', 'shop', 'quantity', 'price', 'rrc_price']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['name', 'category']


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    list_display = ['value', 'product_info', 'parameter']
    list_filter = ['value', 'product_info', 'parameter']


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone']
    list_filter = ['user', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone']


@admin.register(ConfirmEmailToken)
class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    list_display = ['key', 'user', 'created_at']