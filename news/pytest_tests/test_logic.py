from http import HTTPStatus
from random import choice

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.pytest_tests.test_constants import FORM_DATA


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, url_detail):
    """Анононимный пользователь не может добавить комментарий."""
    comment_count = Comment.objects.count()
    client.post(url_detail, FORM_DATA)
    assert Comment.objects.count() == comment_count


def test_user_can_create_comment(author_client, url_detail,
                                 author, news):
    """Залогиненый пользователь может добавить комментарий."""
    Comment.objects.all().delete()
    response = author_client.post(url_detail, FORM_DATA)
    assertRedirects(response, f'{url_detail}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.author == author
    assert comment.news == news


@pytest.mark.django_db
def test_user_cant_use_bad_words(author_client, url_detail):
    """Пользователь не может использовать запрещенные слова в комментраии."""
    comment_count = Comment.objects.count()
    bad_words_data = {'text': f'Текст, {choice(BAD_WORDS)}, еще текст'}
    response = author_client.post(url_detail, data=bad_words_data)
    assert Comment.objects.count() == comment_count
    assertFormError(response, 'form', 'text', errors=WARNING)


def test_author_can_delete_comment(author_client, comment,
                                   url_detail, delete_url):
    """Автор комментрария может удалить его."""
    comment_count = Comment.objects.count()
    response = author_client.delete(delete_url)
    assertRedirects(response, f'{url_detail}#comments')
    assert Comment.objects.count() == comment_count - 1


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(comment, delete_url,
                                                  not_author_client):
    """Пользователь не может удалить чужой комментарий."""
    comment_count = Comment.objects.count()
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comment_count


def test_author_can_edit_comment(author_client, comment, author,
                                 edit_url, url_detail, news):
    """Автор может радактировать свой комментарий."""
    form_data = {'text': 'Изменный текст.'}
    response = author_client.post(edit_url, data=form_data)
    assertRedirects(response, f'{url_detail}#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']
    assert comment.author == author
    assert comment.news == news


def test_user_cant_edit_comment_of_another_user(not_author_client, comment,
                                                edit_url, author, news):
    """Пользователь не может редактировать чужие комментарии."""
    form_data = {'text': 'Изменнный текст.'}
    response = not_author_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_bd = Comment.objects.get(id=comment.id)
    assert comment_from_bd.text == comment.text
    assert comment_from_bd.author == author
    assert comment_from_bd.news == news
