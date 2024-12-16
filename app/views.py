from distutils.util import strtobool
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import URLValidator
from django.db import IntegrityError
from django.http import JsonResponse
from django.db.models import Q, Sum, F
from requests import get
from yaml import load as load_yaml, Loader
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from selenium.webdriver.remote.utils import load_json
from app.tasks import do_import_task
from app.models import ConfirmEmailToken, Category, Shop, Order, OrderItem, Product, Parameter, \
    ProductParameter, Contact, ProductInfo
from app.serializers import UserSerializer, CategorySerializer, ShopSerializer, ProductInfoSerializer, \
    OrderSerializer, OrderItemSerializer, ContactSerializer
from app.signals import new_order
from django.shortcuts import render


class RegisterAccount(APIView):

    def post(self, request, *args, **kwargs):
        if {'first_name', 'last_name', 'email', 'company', 'position'}.issubset(request.data):
            try:
                validate_password(request.data['password'])
            except Exception as password_error:
                password_errors = []
                for error in password_error:
                    password_errors.append(error)
                return JsonResponse({'Status': False, 'Errors': {'password': password_errors}})

            else:
                user_serializer = UserSerializer(data=request.data, context={'user': request.user})
                if user_serializer.is_valid():
                    user = user_serializer.save()
                    user.set_password(request.data['password'])
                    user.save()
                    return JsonResponse({'Status': True})
                else:
                    return JsonResponse({'Status': False, 'errors': user_serializer.errors})

        return JsonResponse({'Status': False, 'error': 'Не заполнены все необходимые поля'})


class ConfirmAccount(APIView):

    def post(self, request, *args, **kwargs):
        if {'email', 'token'}.issubset(request.data):
            token = ConfirmEmailToken.objects.filter(user__email=request.data['email'], key=request.data['token']).first()
            print(token)
            if token:
                token.user.is_active = True
                token.user.save()
                token.delete()
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'errors': 'Неправильно указан токен или email'})

        return JsonResponse({'Status': False, 'error': 'Не заполнены все необходимые поля'})


class AccountDetails(APIView):

    def get(self, request: Request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'error': 'Log in required'}, status=403)
        serializer = UserSerializer(request.user)
        return JsonResponse(serializer.data)

    def post(self, request: Request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'error': 'Log in required'}, status=403)

        if 'password' in request.data:
            errors = {}
            try:
                validate_password(request.data['password'])
            except Exception as password_error:
                errors_array = []
                for error in password_error:
                    errors_array.append(error)
                return JsonResponse({'Status': False, 'Errors': {'password': errors_array}})

        else:
            request.user.set_password(request.data['password'])

        user = UserSerializer(request.user, data=request.data, partial=True)
        if user.is_valid():
            user.save()
            return JsonResponse({'Status': True})
        else:
            return JsonResponse({'Status': False, 'errors': user.errors})


class LoginAccount(APIView):

    
    def post(self, request, *args, **kwargs):

        if {'password', 'email'}.issubset(request.data):
            user = authenticate(request, username=request.data['email'], password=request.data['password'])
            if user is not None:
                if user.is_active == True:
                    token, _ = Token.objects.get_or_create(user=user)
                    return JsonResponse({'Status': True, 'Token': token.key})
            return JsonResponse({'Status':  False, 'Error': 'Authentication failed'})

        return JsonResponse({'Status': False, 'Error': 'All fields required', "Got": request})


class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ShopView(ListAPIView):
    queryset = Shop.objects.filter(state=True)
    serializer_class = ShopSerializer


class ProductInfoView(APIView):

    def get(self, request: Request, *args, **kwargs):
        query = Q(shop__state=True)
        shop_id = request.query_params.get('shop_id')
        category_id = request.query_params.get('category_id')

        if shop_id:
            query = query & Q(shop_id=shop_id)

        if category_id:
            query = query & Q(product__category_id=category_id)

        queryset = ProductInfo.objects.filter(query).select_related('shop', 'product__category').prefetch_related(
                                            'product_parameters__parameter').distinct()
        serializer = ProductInfoSerializer(queryset, many=True)
        return Response(serializer.data)


class BasketView(APIView):

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        basket = Order.objects.filter(user_id=request.user.id, state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()

        serializer = OrderSerializer(basket, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        items_sting = request.data['items']
        if items_sting:
            try:
                items_dict = load_json(items_sting)
            except ValueError:
                return JsonResponse({'Status': False, 'error': 'Incorrect request format'})
            else:
                basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
                objects_created = 0
                for order_item in items_dict:
                    order_item.update({'order': basket.id})
                    serializer = OrderItemSerializer(data=order_item)
                    if serializer.is_valid():
                        try:
                            serializer.save()
                        except IntegrityError as error:
                            return JsonResponse({'Status': False, 'Error': str(error)})
                        else:
                            objects_created += 1
                    else:
                        return JsonResponse({'Status': False, 'Error': serializer.errors})
                return JsonResponse({'Status': True, 'Objects created': objects_created})
        return JsonResponse({'Status': False, 'error': 'All fields required'})

    def delete(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        items_sting = request.data.get('items')
        if items_sting:
            items_list = items_sting.split(',')
            basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
            query = Q()
            objects_deleted = False
            for order_item_id in items_list:
                if order_item_id.isdigit():
                    query = query | Q(order_id=basket.id, id=order_item_id)
                    objects_deleted = True

            if objects_deleted:
                deleted_count = OrderItem.objects.filter(query).delete()[0]
                return JsonResponse({'Status': True, 'Objects deleted:' : deleted_count})
        return JsonResponse({'Status': False, 'Erorr': 'All fields required'})

    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        items_sting = request.data.get('items')
        if items_sting:
            try:
                items_dict = load_json(items_sting)
            except ValueError:
                return JsonResponse({'Status': False, 'Error': 'Incorrect request format'})
            else:
                basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
            objects_updated = 0
            for order_item in items_dict:
                if type(order_item['quantity']) == int and type(order_item['product_info']) == int:
                    objects_updated += OrderItem.objects.filter(order_id=basket.id, id=order_item['product_info']).update(
                        quantity=order_item['quantity'])
            return JsonResponse({'Status': True, 'Updated objects:': objects_updated})

        return JsonResponse({'Status': False, 'Error': 'All fields required'})


class PartnerUpdate(APIView):

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Only for shops'}, status=403)

        url = request.data.get('url')
        if url:
            url_validate = URLValidator()
            try:
                url_validate(url)
            except ValidationError as e:
                return JsonResponse({'Status': False, 'Error': str(e)})
            else:
                user_id = request.user.id
                do_import_task.delay(url, user_id)
                return JsonResponse({'Status': True, 'Message': 'Import task done'})
        return JsonResponse({'Status': False, 'error': 'All fields required'})


class PartnerState(APIView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Only for shops'}, status=403)

        shop = request.user.shop
        shop_serializer = ShopSerializer(shop)
        return Response(shop_serializer.data)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Only for shops'}, status=403)

        state = request.data.get('state')
        if state:
            try:
                Shop.objects.filter(user_id=request.user.id).update(state=strtobool(state))
                return JsonResponse({'Status': True})
            except ValueError as error:
                return JsonResponse({'Status': False, "Error": str(error)})

        return JsonResponse({'Status': False, 'Error': 'All fields required'})


class PartnerOrders(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Only for shops'}, status=403)

        order = (Order.objects.filter(ordered_items__product_info__shop__user_id=request.user.id).exclude(
            state='basket').prefetch_related('ordered_items__product_info__product__category',
                                             'ordered_items__product_info__product_parameters__parameter')
                 .select_related('contact').annotate(total_sum=Sum(F('ordered_items__quantity') *
                                                                   F('ordered_items__product_info__price'))).distinct())
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)


class ContactView(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        contact = Contact.objects.filter(user_id=request.user.id)
        serializer = ContactSerializer(contact, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if {'city', 'street', 'phone'}.issubset(request.data):
            data = request.data.copy()
            data['user'] = request.user.id
            serializer = ContactSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Error': serializer.errors})
        return JsonResponse({'Status': False, 'Error': 'All fields required'})

    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if 'id' in request.data:
            if not isinstance(request.data['id'], int) or request.data['id'] <= 0:
                return JsonResponse({'Status': False, 'Error': "Invalid ID"})
            if request.data['id'] != request.user.id:
                return JsonResponse({'Status': False, 'Error': "Its allowed to change your own contacts only"})
            contact = Contact.objects.filter(id=request.data['id'], user_id=request.user.id).first()
            if contact:
                serializer = ContactSerializer(contact, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'Status': True})
                else:
                    return JsonResponse({'Status': False, 'Error': serializer.errors})
        return JsonResponse({'Status': False, 'Error': 'All fields required'})

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        items_sting = request.data.get('items')
        if items_sting:
            items_list = items_sting.split(',')
            query = Q()
            objects_deleted = False
            for contact_id in items_list:
                if contact_id.isdigit():
                    query = query | Q(user_id=request.user.id, id=contact_id)
                    objects_deleted = True
            if objects_deleted:
                deleted_count = Contact.objects.filter(query).delete()[0]
                return JsonResponse({'Status': True, 'Objects deleted:': deleted_count})
        return JsonResponse({'Status': False, 'Erorr': 'All fields required'})


class OrderView(APIView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        order = Order.objects.filter(user_id=request.user.id).exclude(state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
            total_sum=Sum(F('ordered_items__product_info__price') *
                          F('ordered_items__quantity'))).distinct()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if {'id', 'contact'}.issubset(request.data):
            try:
                contact_id = int(request.data['contact'])
            except ValueError:
                return JsonResponse({'Status': False, 'Error': 'Invalid contact ID'})

            try:
                order = Order.objects.filter(
                        user_id=request.user.id, state='basket').first()
                if order:
                        # Update existing basket order
                    order.contact_id = contact_id
                    order.state = 'new'
                    order.save()
                else:
                        # Create a new order if no basket exists
                    order = Order.objects.create(
                        user_id=request.user.id,
                        contact_id=contact_id,
                        state='new'
                        )
                new_order(sender=self.__class__, user_id=request.user.id)
                return JsonResponse({'Status': True})

            except IntegrityError as err:
                return JsonResponse({'Status': False, 'Error': 'Incorrect data format', 'Error desc': str(err)})

        return JsonResponse({'Status': False, 'Error': 'All fields required'})
