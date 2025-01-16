from rest_framework.authtoken.models import Token
from app.models import User
from urllib.parse import urlencode
from django.shortcuts import redirect

# returns token as redirect url
def auth_complete(request):
    user  = request.user
    token = token, _ = Token.objects.get_or_create(user=user)
    redirect_url = request.GET.get('next', '/')
    separator = '&' if '?' in redirect_url else '?'
    redirect_url += f"{separator}{urlencode({'token': token.key})}" 
    return redirect(redirect_url)
