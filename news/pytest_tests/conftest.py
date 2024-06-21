"""
Какие фикстуры понадобятся для тестирования?
1. test_routes.py
    1. Главная страница доступна анонимному пользователю.
        - фикстура анонимного клиента
    2. Страница отдельной новости доступна анонимному пользователю.
        - фикстура анонимного пользователя
    3. Страницы удаления и редактирования комментария доступны автору комментария
        - пользователь (автор)
        - комментарий
    4. 
"""

import pytest

from django.test.client import Client

from news.models import Comment, News

@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username="Автор")

@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username="Не автор")

@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client

@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client

@pytest.fixture
def news():
    news = News.objects.create(
        title="Название новости.",
        text="Текст новости.",
    )
    return news

@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text="Текст комментария."
    )
    return comment

@pytest.fixture
def comment_id(comment):
    return (comment.id, )
