from rest_framework.permissions import BasePermission

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        print(request.user.role.name)
        if request.user.role.name == "doctor":
            return True
       
    
class IsPatient(BasePermission):
    def has_permission(self, request, view):
        if request.user.role.name == "patient":
            return True
