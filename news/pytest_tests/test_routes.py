from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest import lazy_fixture as fl
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'reverse_url, parametrized_client, status',
    (
        (fl('url_home'), fl('client'), HTTPStatus.OK),
        (fl('url_detail'), fl('client'), HTTPStatus.OK),
        (reverse('users:login'), fl('client'), HTTPStatus.OK),
        (reverse('users:logout'), fl('client'), HTTPStatus.OK),
        (reverse('users:signup'), fl('client'), HTTPStatus.OK),
        (fl('edit_url'), fl('author_client'), HTTPStatus.OK),
        (fl('delete_url'), fl('author_client'), HTTPStatus.OK),
        (fl('edit_url'), fl('not_author_client'), HTTPStatus.NOT_FOUND),
        (fl('delete_url'), fl('not_author_client'), HTTPStatus.NOT_FOUND),
    )
)
def test_availability_pages(reverse_url, parametrized_client, status):
    """Проверка всех маршрутов."""
    response = parametrized_client.get(reverse_url)
    assert response.status_code == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, arg',
    (
        ('news:edit', fl('comment')),
        ('news:delete', fl('comment'))
    )
)
def test_anonim_update_delete_comment(name, client, arg):
    """Тест редиректов.

    Проверка, что анонимного пользователя при попытке
    доступа к страницам: редактирования, удаления комментария
    перебрасывает на страницу логина.
    """
    login_url = reverse('users:login')
    url = reverse(name, args=(arg.id, ))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
