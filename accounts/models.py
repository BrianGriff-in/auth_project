from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.URLField(blank=True, null=True)       # from Google/Facebook
    provider = models.CharField(max_length=50, blank=True) # 'google', 'facebook', 'local'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
from allauth.socialaccount.signals import pre_social_login, social_account_added
from django.dispatch import receiver

@receiver(pre_social_login)
def link_to_existing_user(sender, request, sociallogin, **kwargs):
    """If email already exists, connect social account to it"""
    from allauth.account.models import EmailAddress
    if sociallogin.is_existing:
        return
    
    email = sociallogin.user.email
    if not email:
        return
    
    try:
        existing = EmailAddress.objects.get(email__iexact=email)
        sociallogin.connect(request, existing.user)
    except EmailAddress.DoesNotExist:
        pass

@receiver(social_account_added)
def set_provider_on_signup(sender, request, sociallogin, **kwargs):
    """Set provider and avatar when user signs up via social"""
    user = sociallogin.user
    user.provider = sociallogin.account.provider
    try:
        avatar = sociallogin.account.get_avatar_url()
        if avatar:
            user.avatar = avatar
    except Exception:
        pass
    user.save()

@receiver(pre_social_login)
def set_provider_on_login(sender, request, sociallogin, **kwargs):
    """Update provider and avatar on every social login"""
    if not sociallogin.is_existing:
        return
    user = sociallogin.user
    user.provider = sociallogin.account.provider
    try:
        avatar = sociallogin.account.get_avatar_url()
        if avatar:
            user.avatar = avatar
    except Exception:
        pass
    user.save()