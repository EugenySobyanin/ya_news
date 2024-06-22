from datetime import datetime, timedelta

from django.conf import settings
from django.test.client import Client
from django.utils import timezone
from django.urls import reverse

import pytest

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
def news_id(news):
    return (news.id, )


@pytest.fixture
def all_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='текст',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def comment(news, author, comment_text):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария.'
    )
    return comment


@pytest.fixture
def comment_id(comment):
    return (comment.id, )


@pytest.fixture
def all_comments(author, news):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )

        comment.created = now + timedelta(days=index)
        comment.save()
    return news.comment_set.all()


@pytest.fixture
def url_home():
    return reverse('news:home')


@pytest.fixture
def url_detail(news_id):
    return reverse('news:detail', args=news_id)


@pytest.fixture
def delete_url(comment_id):
    return reverse('news:delete', args=comment_id)


@pytest.fixture
def edit_url(comment_id):
    return reverse('news:edit', args=comment_id)


@pytest.fixture
def comment_text():
    return 'Другой текст комментария.'


@pytest.fixture
def form_data(comment_text):
    return {'text': comment_text}
