import pytest

from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from news.forms import CommentForm
from news.models import Comment, News

User = get_user_model()


@pytest.mark.django_db
def test_news_count(url_home, client, all_news):
    """Проверка количества записей на главной странице."""
    response = client.get(url_home)
    object_list = response.context['object_list']
    assert object_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(url_home, client, all_news):
    """Проверка сортировки новостей на главной странице."""
    response = client.get(url_home)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates
    
@pytest.mark.django_db
def test_comment_order(client, url_detail, all_comments):
    response = client.get(url_detail)
    assert 'news' in response.context
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps
    
    
@pytest.mark.django_db
def test_anonymous_client_has_no_form(url_detail, client):
    response = client.get(url_detail)
    assert 'form' not in response.context
    

@pytest.mark.django_db
def test_authorized_client_has_form(author_client, url_detail):
    response = author_client.get(url_detail)
    assert 'form' in response.context
    
    
