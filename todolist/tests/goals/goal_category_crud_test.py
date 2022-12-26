import pytest

from goals.models import (
    BoardParticipant,
    GoalCategory
)


@pytest.mark.django_db
def test_goal_category_create(auth_client, board_factory):
    board = board_factory(title='test')
    BoardParticipant.objects.create(
        user_id=auth_client.session['_auth_user_id'],
        board=board
    )
    response = auth_client.post(
        '/goals/goal_category/create',
        data={
            'title': 'test',
            'board': board.id,
        }
    )

    assert response.status_code == 201
    assert response.data.get('title') == 'test'


@pytest.mark.django_db
def test_goal_category_list(auth_client, board_factory, goal_category_factory):
    goal_category_count = 10
    board = board_factory(title='test')
    BoardParticipant.objects.create(
        user_id=auth_client.session['_auth_user_id'],
        board=board
    )
    goal_category_factory.create_batch(
        title='test',
        user_id=auth_client.session['_auth_user_id'],
        board=board,
        size=goal_category_count
    )
    response = auth_client.get(
        '/goals/goal_category/list',
    )

    assert response.status_code == 200
    assert len(response.data) == goal_category_count
    for item in response.data:
        assert item.get('title') == 'test'


@pytest.mark.django_db
def test_goal_category_update(auth_client, board_factory):
    board = board_factory(title='test')
    BoardParticipant.objects.create(
        user_id=auth_client.session['_auth_user_id'],
        board=board
    )
    response = auth_client.post(
        '/goals/goal_category/create',
        data={
            'title': 'test',
            'board': board.id,
        }
    )
    pk = response.data.get('id')
    response = auth_client.patch(
        f'/goals/goal_category/{pk}',
        data={
            'title': 'test2',
        },
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.data.get('title') == 'test2'


@pytest.mark.django_db
def test_goal_category_delete(auth_client, board_factory):
    board = board_factory(title='test')
    BoardParticipant.objects.create(
        user_id=auth_client.session['_auth_user_id'],
        board=board
    )
    response = auth_client.post(
        '/goals/goal_category/create',
        data={
            'title': 'test',
            'board': board.id,
        }
    )
    current_count = GoalCategory.objects.filter(is_deleted=False).count()
    pk = response.data.get('id')
    response = auth_client.delete(
        f'/goals/goal_category/{pk}',
    )
    assert response.status_code == 204
    assert GoalCategory.objects.filter(is_deleted=False).count() == current_count - 1
