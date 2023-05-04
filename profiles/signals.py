from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# The 'signal' is a communication between 'sender' and 'receiver' applications. 
# The sender will signal to the receiver to create its own automatically.
# In this case, User creation will be the sender to Profile to create the profile of the user automatically.

# The receiver decorator (first argument is the signal)
@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    # 'sender' is the class of django.contrib.auto.models.User
    # 'instance' is the user created or updated to have a profile matched automatically
    # 'created or updated', it signals to the profile. Therefore, 'created' must be checked to create the profile only once.
    if created:
        Profile.objects.create(user=instance)

# secondly, go to 'apps.py' to configure the Profile app to receive the signal
# finally, go to '__init__.py' to initialize the configuration of the signal communication