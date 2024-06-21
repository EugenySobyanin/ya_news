import pytest

from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
def test_home_page_for_anonim_user(client):
    # Доступ анонимного пользователя к главной странице
    url = reverse('news:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_news_for_anonim_user(client, news):
    # Доступ анонимного пользователя к новости
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args', 
    (('news:edit', pytest.lazy_fixture('comment_id')) ,('news:delete', pytest.lazy_fixture('comment_id')))
)
def test_autho_update_delete_comment(name, args, author_client):
    # Доступ автора к редактированию и удалению комментариев
    url = reverse(name, args=args)
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (('news:edit', pytest.lazy_fixture('comment_id')) ,('news:delete', pytest.lazy_fixture('comment_id')))
)
def test_anonim_update_delete_comment(name, args, client):
    # Доступ анонимного пользователя к редактированию, удалению комментариев
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
    

@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (('news:edit', pytest.lazy_fixture('comment_id')) ,('news:delete', pytest.lazy_fixture('comment_id')))
)
def test_not_author_update_delete_comment(name, args, not_author_client):
    # Дотступ не автора комментария к его редактированию и удалению
    url = reverse(name, args=args)
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('users:login', 'users:logout', 'users:signup')
)
def test_anonim_login_logout_signup(name, client):
    # Доступ анонимного пользователя к страницам входа, выхода, регистрации
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

    




"""На отправку."""