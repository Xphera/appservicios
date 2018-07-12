from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from prestadores.models import Prestador

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
       
        if(user.groups.filter(name='cliente').exists()):
            print('cliente')
        if(user.groups.filter(name='administrador').exists()):
            print('administrador')
        else:
            p = Prestador.objects.get(user=user)
            fullname=''
            fullname=p.nombres+' '+p.primerApellido+' '+p.segundoApellido

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'fullname':fullname
        })