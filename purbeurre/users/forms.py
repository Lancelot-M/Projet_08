"""Formulaire file"""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    """Creation user data model"""
    class Meta(UserCreationForm.Meta):
        """add email to creation model"""
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("email",)
