from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Category
from .forms import CategoryForm


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'categories/category_list.html'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('category-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('category-list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


    def dispatch(self, request, *args, **kwargs):
        category = self.get_object()
        if category.is_system:
            messages.error(request, "Nie można edytować kategorii systemowej")
            return redirect('category-list')
        return super().dispatch(request, *args, **kwargs)

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')
    template_name = 'categories/category_confirm_delete.html'

    def get_queryset(self):
        # Wykluczamy kategorie systemowe z możliwości usunięcia
        return Category.objects.filter(is_system=False)

    def dispatch(self, request, *args, **kwargs):
        category = self.get_object()
        if category.is_system:
            messages.error(request, "Nie można usunąć kategorii systemowej")
            return redirect('category-list')
        return super().dispatch(request, *args, **kwargs)
