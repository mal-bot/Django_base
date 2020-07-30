from django.shortcuts import render
from json import load
import os
from geekshop.settings import BASE_DIR
from .models import Product, ProductCategory


def main(request):
    content_products = Product.objects.all()[:4]
    context = {

        'title': 'главная',
        'main_menu': [
                        {'href': 'main', 'name': 'домой'},
                        {'href': 'products', 'name': 'продукты'},
                        {'href': 'contacts', 'name': 'контакты'}
                    ],
        'content_products': content_products
    }
    # file_path = os.path.join(
    #     BASE_DIR, 'mainapp/contexts_lesson_2/main_context.json')
    # if os.path.exists(file_path):
    #     with open(file_path) as file:
    #         context = load(file)
    return render(request, 'mainapp/index.html', context)


def products(request):
    file_path = os.path.join(
        BASE_DIR, 'mainapp/contexts_lesson_2/products_context.json')
    if os.path.exists(file_path):
        with open(file_path) as file:
            context = load(file)

    return render(request, 'mainapp/products.html', context)


def contacts(request):
    file_path = os.path.join(
        BASE_DIR, 'mainapp/contexts_lesson_2/contacts_context.json')
    if os.path.exists(file_path):
        with open(file_path) as file:
            context = load(file)
        return render(request, 'mainapp/contact.html', context)
