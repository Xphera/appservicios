from rest_framework import permissions

from  clientes.models import Ubicacion
class EsDueño(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
       
        #if request.method in permissions.SAFE_METHODS:
        #   return True

        # Write permissions are only allowed to the owner of the snippet.
        if(type(obj) == Ubicacion):
            return obj.cliente.user == request.user
        else:
            return obj.user == request.user


    def has_permission(self, request, view):
        return True