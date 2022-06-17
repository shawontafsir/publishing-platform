from users.models import User


class UserDataLayer:

    @classmethod
    def create_user(cls, **kwargs):
        return User.objects.create_user(**kwargs)
