from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(object):
    def authenticate(self, username=None, password=None, ignore_password=None):

        User = get_user_model()

        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            if ignore_password or user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):

        User = get_user_model()

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None