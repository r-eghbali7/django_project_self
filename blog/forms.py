from django import forms
from django.core.validators import MinLengthValidator, EmailValidator, RegexValidator


class BaseCommentFields(forms.Form):
    NAME_VALIDATORS = [
        MinLengthValidator(2, 'Name must be at least 2 characters long'),
        RegexValidator(
            regex=r'^[a-zA-Z\s\u0600-\u06FF]+$',
            message='Name can only contain letters and spaces'
        )
    ]
    
    EMAIL_VALIDATORS = [
        RegexValidator(
            regex=r'^[a-zA-Z0-9._%+-]+@gmail\.com$',
            message='Email must be a valid Gmail address'
        )
    ]
    
    BODY_VALIDATORS = [
        MinLengthValidator(5, 'Comment must be at least 5 characters long'),
        RegexValidator(
            regex=r'^[a-zA-Z0-9\s\u0600-\u06FF.,!?()-]+$',
            message='Comment contains invalid characters'
        )
    ]



class CommentForm(forms.Form):
    name = forms.CharField(
        label='نام',
        max_length=80,
        validators=BaseCommentFields.NAME_VALIDATORS,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='ایمیل',
        validators=BaseCommentFields.EMAIL_VALIDATORS,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    body = forms.CharField(
        label='متن',
        validators=BaseCommentFields.BODY_VALIDATORS,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

class ReplyCommentForm(forms.Form):
    name = forms.CharField(
        label='نام',
        max_length=80,
        validators=BaseCommentFields.NAME_VALIDATORS,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='ایمیل',
        validators=BaseCommentFields.EMAIL_VALIDATORS,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    body = forms.CharField(
        label='متن',
        validators=BaseCommentFields.BODY_VALIDATORS,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    