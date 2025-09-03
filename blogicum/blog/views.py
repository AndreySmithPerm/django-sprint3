from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Category, Post

POST_LIMIT = 5


def basic_set(manager=Post.objects):
    """Базовый набор выбранных постов"""
    return (
        manager.select_related('author', 'category', 'location')
        .filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        ).order_by('-pub_date')
    )


def index(request):
    """Главная страница"""
    # Получаем последние опубликованные посты по условиям
    post_list = basic_set()[:POST_LIMIT]
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """Отображение описания выбранной записи"""
    post = get_object_or_404(
        Post.objects.select_related('category')
        .filter(id=post_id, is_published=True,
                pub_date__lte=timezone.now(), category__is_published=True)
    )

    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """Отображение постов категории"""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    # Получаем опубликованные посты данной категории
    post_list = basic_set(manager=Post.objects.filter(category=category))

    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)
