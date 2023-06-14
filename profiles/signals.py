from .models import Profile, Relationship
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

# The 'signal' is a communication between 'sender' and 'receiver' applications. 
# The sender will signal to the receiver to create its own automatically.
# In this case, User creation will be the sender to Profile to create the profile of the user automatically.

# The receiver decorator (first argument is the signal)
@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    # 'sender' is the class of django.contrib.auto.models.User (e.g., the model)
    # 'instance' is the user (object) created or updated to have a profile matched automatically
    # 'created', it signals to this to create a profile. Therefore, 'created' must be checked to create the profile only once.
    if created: # this is passed as 'True', only when the object (instance) is created only once.
        Profile.objects.create(user=instance)

# secondly, go to 'apps.py' to configure the Profile app to receive the signal
# finally, go to '__init__.py' to initialize the configuration of the signal communication

@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, **kwargs):
    # 'sender' in parameter is the model (Relationship) which is signaling to this
    # 'instance' is the object just created or updated in Relationship 
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()

@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_from_friends(sender, instance, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if receiver_.user in sender_.friends.all(): # Be careful, friends in Profile is 'User' model, not 'Profile' model
        sender_.friends.remove(receiver_.user)
        sender_.save()

    if sender_.user in receiver_.friends.all(): # Be careful, friends in Profile is 'User' model, not 'Profile' model
        receiver_.friends.remove(sender_.user)
        receiver_.save()

