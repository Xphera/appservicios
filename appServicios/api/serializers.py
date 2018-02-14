from django.contrib.auth.models import User
from rest_framework import serializers

from clientes.models import Cliente
from prestadores.models import Prestador


class UserSerializer(serializers.ModelSerializer):
    clientes = serializers.PrimaryKeyRelatedField(many=True, queryset=Cliente.objects.all())
    prestadores = serializers.PrimaryKeyRelatedField(many=True, queryset=Prestador.objects.all())
    class Meta:
        model = User
        fields = ('id', 'username', 'clientes','prestadores')


