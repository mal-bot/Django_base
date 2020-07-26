from django.shortcuts import render
from json import load


def main(request):
    with open(r'mainapp\contexts_lesson_2\main_context.json', 'r') as file:
        context = load(file)
    return render(request, 'mainapp/index.html', context)


def products(request):
    with open(r'mainapp\contexts_lesson_2\products_context.json', 'r') as file:
        context = load(file)
    return render(request, 'mainapp/products.html', context)


def contacts(request):
    with open(r'mainapp\contexts_lesson_2\contacts_context.json', 'r') as file:
        context = load(file)
    return render(request, 'mainapp/contact.html', context)