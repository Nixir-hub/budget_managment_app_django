from django.urls import path
from .views import CategoryDeleteView, CategoryUpdateView, CategoryCreateView, CategoryListView

urlpatterns = [
path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category-add'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
]