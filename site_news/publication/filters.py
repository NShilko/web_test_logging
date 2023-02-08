from django_filters import FilterSet, DateFilter, CharFilter
from .models import Post
from django import forms


class PostFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters['title'].label = "Название содержит"
        self.filters['isCategory'].label = "Категория"
        self.filters['date'].label = "Опубликованы позже"

    date = DateFilter(widget=forms.DateInput(attrs={'type': 'date'}), lookup_expr='gt')
    title = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['title', 'isCategory', 'date']
