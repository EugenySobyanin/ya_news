from django.conf import settings

import pytest


@pytest.mark.django_db
def test_news_count(url_home, client, all_news):
    """Проверка количества записей на главной странице."""
    response = client.get(url_home)
    object_list = response.context['object_list']
    assert object_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(url_home, client, all_news):
    """Сортировки новостей на главной странице."""
    response = client.get(url_home)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comment_order(client, url_detail, all_comments):
    """Сортировка комментариев."""
    response = client.get(url_detail)
    assert 'news' in response.context
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_anonymous_client_has_no_form(url_detail, client):
    """Анонимный пользователь не получает форму комментария."""
    response = client.get(url_detail)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(author_client, url_detail):
    """Авторизированный полльзователь получает форму комментария."""
    response = author_client.get(url_detail)
    assert 'form' in response.context
