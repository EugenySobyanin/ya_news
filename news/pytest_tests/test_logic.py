from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, url_detail, form_data):
    """Анононимный пользователь не может добавить комментарий."""
    client.post(url_detail, form_data)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(author_client, url_detail,
                                 form_data, author, news, comment_text):
    """Залогиненый пользователь может добавить комментарий."""
    response = author_client.post(url_detail, form_data)
    assertRedirects(response, f'{url_detail}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == comment_text
    assert comment.author == author
    assert comment.news == news


@pytest.mark.django_db
def test_user_cant_use_bad_words(author_client, url_detail):
    """Пользователь не может использовать запрещенные слова в комментраии."""
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url_detail, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, comment,
                                   url_detail, delete_url):
    """Автор комментрария может удалить его."""
    response = author_client.delete(delete_url)
    assertRedirects(response, f'{url_detail}#comments')
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(comment, delete_url,
                                                  not_author_client):
    """Пользователь не может удалить чужой комментарий."""
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(author_client, comment, form_data,
                                 edit_url, url_detail):
    """Автор может радактировать свой комментарий."""
    form_data['text'] = 'Измененный текст.'
    response = author_client.post(edit_url, data=form_data)
    assertRedirects(response, f'{url_detail}#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_user_cant_edit_comment_of_another_user(not_author_client, comment,
                                                edit_url, form_data):
    """Пользователь не может редактировать чужие комментарии."""
    comment_text = comment.text
    form_data['text'] = 'Изменный текст.'
    response = not_author_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment.text == comment_text
