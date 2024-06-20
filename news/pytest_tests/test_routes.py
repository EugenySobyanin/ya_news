import pytest

from http import HTTPStatus

from django.urls import reverse

@pytest.mark.django_db
def test_home_page_for_anonim_user(client):
    # пункт 1
    url = reverse('news:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

@pytest.mark.django_db
def test_news_for_anonim_user(client, news):
    # пункт 2
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
