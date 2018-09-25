from django import forms

from .models import Community


class CreateCommunity(forms.ModelForm):
    model = Community


class ManageCommunityForm(forms.ModelForm):
    model = Community

    
    # dropdown: active community
    # multidropdown: manager (exclude self
    # 