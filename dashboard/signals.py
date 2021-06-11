from .models import Client, Driver
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
#
#
# def client_profile(sender, instance, create, **kwargs):
#     if create:
#         group = Group.objects.get(name="Client")
#         instance.group.add(group)
#
#         Client.objects.create(
#             user=instance,
#             # name=instance.username,
#             gender=instance.gender,
#             date_of_birth = instance.date_of_birth,
#             address = instance.address,
#             phone_number = instance.phone_number
#         )
#
#
# post_save.connect(client_profile, sender=User)

# @receiver(post_save, sender=User)


def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
    print("Token created.")


post_save.connect(create_auth_token, sender=User)