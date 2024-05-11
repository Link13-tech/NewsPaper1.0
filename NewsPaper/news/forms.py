from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'author',
            'categories',
            'title',
            'content',
        )

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        if content is not None and len(content) < 35:
            raise ValidationError({
                "content": "Пост не может быть менее 35 символов."
            })

        return cleaned_data
