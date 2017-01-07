from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# auth backend что бы пользователи могли логинится с помощью email
class EmailBackend(object):

    def authenticate(self, username=None, password=None, **kwargs):
        # в данный момент используется стандартная userModel - User
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and user.check_password(password):
                return user
        return None

    # без этого метода, этод backend не работает
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None