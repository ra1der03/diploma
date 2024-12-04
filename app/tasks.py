from celery import shared_task
from django.http import JsonResponse
from requests import get
from yaml import load as load_yaml, Loader
from app.models import  Category, Shop,  Product, Parameter, ProductParameter, ProductInfo
from django.core.mail import EmailMultiAlternatives


@shared_task
def password_reset_task(email_, token_, set_):
    msg = EmailMultiAlternatives(
        f"Password reset token for {email_}",
        token_,
        set_,
        [email_]
    )
    msg.send()


@shared_task
def new_user_task(email_, token_, set_):
    msg = EmailMultiAlternatives(
            f"Password reset token for {email_}",
            token_,
            set_,
            [email_]
        )
    msg.send()


@shared_task
def new_order_task(email_, token_, set_):
    msg = EmailMultiAlternatives(
        "Обновление статуса заказа",
    "Заказ сформирован",
    set_,
        [email_])
    msg.send()


@shared_task
def do_import_task(url, user_id):
    stream = get(url).content
    data = load_yaml(stream, Loader=Loader)
    shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=user_id)
    for category in data['categories']:
        category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
        category_object.shops.add(shop.id)
        category_object.save()
    ProductInfo.objects.filter(shop_id=shop.id).delete()
    for item in data['goods']:
        product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])
        product_info = ProductInfo.objects.create(product_id=product.id, external_id=item['id'],
                                                  model=item['model'], quantity=item['quantity'],
                                                  price=item['price'], price_rrc=item['price_rrc'], shop_id=shop.id)
        for name, value in item['parameters'].items():
            parameter_object, _ = Parameter.objects.get_or_create(name=name)
            ProductParameter.objects.create(product_info_id=product_info.id,
                                            parameter_id=parameter_object.id, value=value)