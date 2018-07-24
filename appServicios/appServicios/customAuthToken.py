from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from utils.Utils.usuario import Usuario
# from prestadores.models import Prestador
# from clientes.models import Cliente

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        u = Usuario()
        return Response(
            u.infoToken(user)
        )
        
        # token, created = Token.objects.get_or_create(user=user)
       
        # if(user.groups.filter(name='cliente').exists()):
        #     c = Cliente.objects.get(user=user)
        #     fullname=str(c.nombres)+' '+str(c.primerApellido)+' '+str(c.segundoApellido)
        # elif(user.groups.filter(name='administrador').exists()):
        #     print('administrador')
        # else:
        #     p = Prestador.objects.get(user=user)
        #     fullname=p.nombres+' '+p.primerApellido+' '+p.segundoApellido

        # return Response({
        #     'token': token.key,
        #     'user_id': user.pk,
        #     'email': user.email,
        #     'fullname':fullname
        # })