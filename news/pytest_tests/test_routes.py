import pytest

from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects


# @pytest.mark.django_db
# def test_home_page_for_anonim_user(client):
#     # 1. Доступ анонимного пользователя к главной странице
#     url = reverse('news:home')
#     response = client.get(url)
#     assert response.status_code == HTTPStatus.OK


# @pytest.mark.django_db
# def test_news_for_anonim_user(client, news):
#     # 2. Доступ анонимного пользователя к новости
#     url = reverse('news:detail', args=(news.id,))
#     response = client.get(url)
#     assert response.status_code == HTTPStatus.OK


# @pytest.mark.django_db
# @pytest.mark.parametrize(
#     'name, args', 
#     (('news:edit', pytest.lazy_fixture('comment_id')) ,('news:delete', pytest.lazy_fixture('comment_id')))
# )
# def test_autho_update_delete_comment(name, args, author_client):
#     # 3. Доступ автора к редактированию и удалению комментариев
#     url = reverse(name, args=args)
#     response = author_client.get(url)
#     assert response.status_code == HTTPStatus.OK


# @pytest.mark.django_db
# @pytest.mark.parametrize(
#     'name, args',
#     (('news:edit', pytest.lazy_fixture('comment_id')) ,('news:delete', pytest.lazy_fixture('comment_id')))
# )
# def test_anonim_update_delete_comment(name, args, client):
#     # 4. Доступ анонимного пользователя к редактированию, удалению комментариев
#     login_url = reverse('users:login')
#     url = reverse(name, args=args)
#     expected_url = f'{login_url}?next={url}'
#     response = client.get(url)
#     assertRedirects(response, expected_url)
    

# @pytest.mark.django_db
# @pytest.mark.parametrize(
#     'name, args',
#     (('news:edit', pytest.lazy_fixture('comment_id')) ,('news:delete', pytest.lazy_fixture('comment_id')))
# )
# def test_not_author_update_delete_comment(name, args, not_author_client):
#     # 5. Дотступ не автора комментария к его редактированию и удалению
#     url = reverse(name, args=args)
#     response = not_author_client.get(url)
#     assert response.status_code == HTTPStatus.NOT_FOUND


# @pytest.mark.django_db
# @pytest.mark.parametrize(
#     'name',
#     ('users:login', 'users:logout', 'users:signup')
# )
# def test_anonim_login_logout_signup(name, client):
#     # 6. Доступ анонимного пользователя к страницам входа, выхода, регистрации
#     url = reverse(name)
#     response = client.get(url)
#     assert response.status_code == HTTPStatus.OK

# объединить 1, 2, 6
# объединить 3, 5   




"""На отправку."""


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('news_id')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    )
)
def test_pages_availability(name, args, client):
    """Доступность страниц анонимному пользователю."""
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND)
    )
)
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('comment_id')),
        ('news:delete', pytest.lazy_fixture('comment_id'))
    )
)
def test_availability_for_comment_edit_and_delete(parametrized_client,
                                                  expected_status, name, args):
    """Доступ к страницам редактирования и удаления комментария.

    Проверка, что редактировать и удалять комментарии может
    только их автор, а другому пользователю вернется ошибка 404.
    """
    url = reverse(name, args=args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('comment_id')),
        ('news:delete', pytest.lazy_fixture('comment_id'))
    )
)
def test_anonim_update_delete_comment(name, args, client):
    """Тест редиректов.

    Проверка, что анонимного пользователя при попытке
    доступа к страницам: редактирования, удаления комментария
    перебрасывает на страницу логина.
    """
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
