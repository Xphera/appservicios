from django.contrib.auth.models import User
from rest_framework import serializers

from clientes.models import Cliente
from prestadores.models import Prestador


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


