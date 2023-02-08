from django.urls import path
from .views import ArticlesDetail, PublList, ArticlesUpdate, ArticlesCreate, ArticlesDelete

urlpatterns = [
    path('<int:pk>', ArticlesDetail.as_view(), name='articles_detail'),
    path("", PublList.as_view(), name='articles_list'),
    path('create/', ArticlesCreate.as_view(), name='articles_create'),
    path('<int:pk>/update/', ArticlesUpdate.as_view(), name='articles_update'),
    path('<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
]
