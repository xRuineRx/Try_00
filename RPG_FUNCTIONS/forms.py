from django import forms
from .models import GamePost, GamePost_message
from ckeditor.fields import RichTextFormField

class GamePostForm(forms.ModelForm):
    class Meta:
        model = GamePost
        fields = [
            'header',
            'text',
            'CategoryCheck',
            'body',
        ]
        widgets = {
            'body': RichTextFormField(config_name='default'),
        }


class GamePostOtklickForm(forms.ModelForm):
    class Meta:
        model = GamePost_message
        fields = [
            'text_message',
            'text_message_senders',

        ]

