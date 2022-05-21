from django.contrib.auth.models import User


from authentication import models


class UsernameProfileConverter:
    regex = ''

    def to_python(self, value):
        user = User.objects.get(username=value)
        profile = user.profile

        return profile
    
    def to_url(self, value):
        profile = value
        username = profile.user.username

        return username