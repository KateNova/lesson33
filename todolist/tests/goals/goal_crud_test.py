from django.utils import timezone

import pytest

from goals.models import (
    BoardParticipant,
    Goal
)


@pytest.mark.django_db
def test_goal_create(auth_client, board_factory, goal_category_factory):
    board = board_factory(title='test')
    BoardParticipant.objects.create(
        user_id=auth_client.session['_auth_user_id'],
        board=board
    )
    category = goal_category_factory(
        title='test',
        user_id=auth_client.session['_auth_user_id'],
        board=board
    )
    response = auth_client.post(
        '/goals/goal/create',
        data={
            'title': 'test',
            'category': category.id,
            'due_date': timezone.now().strftime('%Y-%m-%d')
        }
    )

    assert response.status_code == 201
    assert response.data.get('title') == 'test'


@pytest.mark.django_db
def test_goal_list(auth_client, board_factory, goal_category_factory, goal_factory):
    goals_count = 10
    board = board_factory(title='test')
    BoardParticipant.objects.create(
        user_id=auth_client.session['_auth_user_id'],
        board=board
    )
    category = goal_category_factory(
        title='test',
        user_id=auth_client.session['_auth_user_id'],
        board=board
    )
    goal_factory.create_batch(
        size=goals_count,
        title='test',
        user_id=auth_client.session['_auth_user_id'],
        category=category
    )
    response = auth_client.get(
        '/goals/goal/list',
    )

    assert response.status_code == 200
    assert len(response.data) == goals_count
    for item in response.data:
        assert item.get('title') == 'test'


@pytest.mark.django_db
def test_goal_update(auth_client, board_factory, goal_category_factory):
    board = board_factory(title='test')
    BoardParticipant.objects.create(
        user_id=auth_client.session['_auth_user_id'],
        board=board
    )
    category = goal_category_factory(
        title='test',
        user_id=auth_client.session['_auth_user_id'],
        board=board
    )
    response = auth_client.post(
        '/goals/goal/create',
        data={
            'title': 'test',
            'category': category.id,
            'due_date': timezone.now().strftime('%Y-%m-%d')
        }
    )
    pk = response.data.get('id')
    response = auth_client.patch(
        f'/goals/goal/{pk}',
        data={
            'title': 'test2',
        },
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.data.get('title') == 'test2'


@pytest.mark.django_db
def test_goal_delete(auth_client, board_factory, goal_category_factory):
    board = board_factory(title='test')
    BoardParticipant.objects.create(
        user_id=auth_client.session['_auth_user_id'],
        board=board
    )
    category = goal_category_factory(
        title='test',
        user_id=auth_client.session['_auth_user_id'],
        board=board
    )
    response = auth_client.post(
        '/goals/goal/create',
        data={
            'title': 'test',
            'category': category.id,
            'due_date': timezone.now().strftime('%Y-%m-%d')
        }
    )
    current_count = Goal.objects.filter(is_deleted=False).count()
    pk = response.data.get('id')
    response = auth_client.delete(
        f'/goals/goal/{pk}',
    )
    assert response.status_code == 204
    assert Goal.objects.filter(is_deleted=False).count() == current_count - 1
