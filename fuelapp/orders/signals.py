# This has been HELL!!!!
# I'll leave it here for "Nostalgia"
# Ideally this was the one to create a user and update them, but 
# I was doing it manually and also triggering the signals to create a user at the 
# same time



# signals.py will be used by the navbar to determine
# what to present to different user types

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models import UserProfile # Importing my UserProfile model for models.py file


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and not instance.is_superuser:
#         UserProfile.objects.create(user=instance)  # Only create if it doesn't exist
#     elif hasattr(instance, 'userprofile'):
#         instance.userprofile.save()  # Update profile on user change

# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created and not instance.is_superuser:
#         # Check if the profile exists, and create if it doesn't
#         if not hasattr(instance, 'userprofile'):
#             UserProfile.objects.create(user=instance)  # Avoid using get_or_create
#     elif not instance.is_superuser:
#         instance.userprofile.save()  # Ensure the profile is updated on user changes



# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and not instance.is_superuser:
#         # Create profile only if it doesn't already exist
#         profile, created = UserProfile.objects.get_or_create(user=instance)
#         if created:
#             print(f"Profile created for user {instance.username} with default type: {profile.user_type}")
#         else:
#             print(f"Profile already exists for user {instance.username}")
    
    
    # elif hasattr(instance, 'userprofile') and not instance.is_superuser:
        # Update profile if already exists
        # profile = instance.userprofile
        # Check what fields are being updated
        # print(f"Updating profile for user {instance.username}. Current type: {profile.user_type}")
         # Save any changes if needed (if we have logic that modifies the profile)
        # profile.save()
        # Avoid unnecessary saves unless there's a real update
        # if instance._state.adding is False:
        #     instance.userprofile.save()
        #     print(f"Profile updated for user {instance.username}")



# Second comment out
# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     # Debugging
#     print(f"Signal received: User {instance.username}, created: {created}")

#     if created and not instance.is_superuser:
#         profile, _ = UserProfile.objects.get_or_create(user=instance)
#     elif not instance.is_superuser:
#         instance.userprofile.save() # Ensure profile is saved on user updates.
#         print(f"Profile updated for user {instance.username}") # Debugging

# First comment out
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.get_or_create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     if hasattr(instance, 'userprofile'):
#         instance.userprofile.save()