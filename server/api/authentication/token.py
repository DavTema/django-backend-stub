from rest_framework.authentication import TokenAuthentication

from api.models import CustomToken


class CustomTokenAuthentication(TokenAuthentication):
    keyword = 'Token'
    model = CustomToken
