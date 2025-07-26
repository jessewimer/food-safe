from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'email', 'city', 'content']  # Added 'email' here
        widgets = {
            'author_name': forms.TextInput(attrs={
                'placeholder': 'Your name (optional)',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={  # This is correct
                'placeholder': 'Your email (optional)',
                'class': 'form-control'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'Your city (optional)',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Your message *',
                'class': 'form-control',
                'required': True
            })
        }