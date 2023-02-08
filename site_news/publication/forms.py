from django import forms
from django.core.exceptions import ValidationError
from .models import Post

FIELDS = [
            'isAuthor',
            'title',
            'main_text',
            'isCategory',
            'kind',
        ]

LABELS = {
    'isCategory': 'Категория',
    'isAuthor': 'Автор статьи'
}


class NewsForm(forms.ModelForm):

    main_text = forms.CharField(min_length=20, widget=forms.Textarea, label='Описание')
    title = forms.CharField(min_length=5, label='Название новости')
    kind = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'NEWS'}))

    class Meta:
        model = Post
        fields = FIELDS
        labels = LABELS

    def clean(self):
        cleaned_data = super().clean()
        main_text = cleaned_data.get("main_text")
        title = cleaned_data.get("title")

        if title == main_text:
            raise ValidationError({
                "title": "Описание не должно быть идентично названию."
            })

        return cleaned_data


class ArticlesForm(forms.ModelForm):
    main_text = forms.CharField(min_length=20, widget=forms.Textarea, label='Описание')
    title = forms.CharField(min_length=5, label='Название статьи')
    kind = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'PUBL'}))

    class Meta:
        model = Post
        fields = FIELDS
        labels = LABELS

    def clean(self):
        cleaned_data = super().clean()
        main_text = cleaned_data.get("main_text")
        title = cleaned_data.get("title")

        if title == main_text:
            raise ValidationError({
                "title": "Описание не должно быть идентично названию."
            })

        return cleaned_data
