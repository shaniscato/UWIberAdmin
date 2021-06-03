# from .models import Client, Driver
# from django.contrib.auth.models import User, Group
# from django.db.models.signals import post_save
#
#
# def client_profile(sender, instance, create, **kwargs):
#     if create:
#         group = Group.objects.get(name="Client")
#         instance.group.add(group)
#
#         Client.objects.create(
#             user=instance,
#             name=instance.username,
#         )
#
#
# post_save.connect(client_profile, sender=User)
