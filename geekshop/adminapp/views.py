from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory
from adminapp.forms import ProductCategoryEditForm, ShopUserAdminEditForm, ProductEditForm
from django.core.paginator import Paginator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.decorators import method_decorator



# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'пользователи'
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#     context = {
#         'title': title,
#         'objects': users_list
#     }
#     return render(request, 'adminapp/users.html', context)

class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(is_active=True)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи/создание'
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegisterForm()
    context = {'title': title, 'update_form': user_form}
    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/редактирование'
    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)
    context = {'title': title, 'update_form': edit_form}
    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователи/удаление'
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))
    context = {
        'title': title,
        'user_to_delete': user
    }
    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'
    categories_list = ProductCategory.objects.all()
    context = {
        'title': title,
        'objects': categories_list
    }
    return render(request, 'adminapp/categories.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'категории/создание'
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST, request.FILES)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         category_form = ProductCategoryEditForm()
#     context = {'title': title, 'update_form': category_form}
#     return render(request, 'adminapp/category_update.html', context)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    # fields = '__all__'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'категории/редактирование'
#
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin:category_update', args=[edit_category.pk]))
#     else:
#         edit_form = ProductCategoryEditForm(instance=edit_category)
#     context = {'title': title, 'update_form': edit_form}
#     return render(request, 'adminapp/category_update.html', context)

class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     title = 'категории/удаление'
#     category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         if category.is_active:
#             category.is_active = False
#         else:
#             category.is_active = True
#         category.save()
#         return HttpResponseRedirect(reverse('admin:categories'))
#     context = {'title': title, 'category_to_delete': category}
#     return render(request, 'adminapp/category_delete.html', context)

class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/удаление'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())




@user_passes_test(lambda u: u.is_superuser)
def products(request, pk, page=1):
    title = 'админка/продукт'
    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    paginator = Paginator(products_list, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'category': category,
        'objects': products_paginator,
    }
    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'продукт/создание'
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[product.category.pk]))
    else:
        product_form = ProductEditForm()
    context = {
        'title': title,
        'update_form': product_form,
        'category': category
    }
    return render(request, 'adminapp/product_update.html', context)



# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     title = 'продукт'
#     product = get_object_or_404(Product, pk=pk)
#
#     context = {
#         'title': title,
#         'object': product
#     }
#     return render(request, 'adminapp/product_read.html', context)


class ProductDetailesView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт/редактирование'
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:product_update', args=[product.pk]))
    else:
        edit_form = ProductEditForm(instance=product)
    context = {
        'title': title,
        'update_form': edit_form,
        'category': product.category
    }

    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукт/удаление'
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        if product.is_active:
            product.is_active = False
        else:
            product.is_active = True
        product.save()
        return HttpResponseRedirect(reverse('admin:products', args=[product.category.pk]))
    context = {
        'title': title,
        'product_to_delete': product
    }
    return render(request, 'adminapp/product_delete.html', context)

