from django.contrib.auth import get_user_model
from django.db import models as m


User = get_user_model()


class Token(m.Model):
    user = m.ForeignKey(User, on_delete=m.CASCADE)
    value = m.CharField(max_length=256)
    time_created = m.DateTimeField(auto_now_add=True)
    # TODO : time_expired


class ProfilePicture(m.Model):
    profile = m.ForeignKey('UserProfile', on_delete=m.CASCADE)
    file = m.ImageField(upload_to='profile-pictures')
    time_created = m.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.url


class UserProfile(m.Model):
    user = m.OneToOneField(User, on_delete=m.CASCADE, primary_key=True, related_name='profile')
    nickname = m.CharField(max_length=40)
    updated_time = m.DateTimeField(auto_now=True)
    picture = m.ForeignKey(ProfilePicture, on_delete=m.CASCADE, null=True, blank=True, related_name='profile_picture')

    def __str__(self):
        return self.nickname

    def clear_contents(self):
        self.nickname = ''
        self.save()
