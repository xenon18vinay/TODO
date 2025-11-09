from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(
        self, request, username = None, password = None, **kwargs
    ):
        try:
            user= UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None