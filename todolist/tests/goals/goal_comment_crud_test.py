import pytest

from goals.models import (
    BoardParticipant,
    GoalComment
)


@pytest.mark.django_db
def test_goal_comment_create(auth_client, board_factory, goal_category_factory, goal_factory):
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
    goal = goal_factory(
        title='test',
        category=category,
        user_id=auth_client.session['_auth_user_id'],
    )
    response = auth_client.post(
        '/goals/goal_comment/create',
        data={
            'text': 'test',
            'goal': goal.id,
        }
    )

    assert response.status_code == 201
    assert response.data.get('text') == 'test'


@pytest.mark.django_db
def test_goal_comments_list(
        auth_client,
        board_factory,
        goal_category_factory,
        goal_factory,
        goal_comment_factory
):
    goal_comments_count = 10
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
    goal = goal_factory(
        title='test',
        user_id=auth_client.session['_auth_user_id'],
        category=category
    )
    goal_comment_factory.create_batch(
        size=goal_comments_count,
        goal=goal,
        user_id=auth_client.session['_auth_user_id'],
    )
    response = auth_client.get(
        '/goals/goal_comment/list',
    )

    assert response.status_code == 200
    assert len(response.data) == goal_comments_count
    for item in response.data:
        assert item.get('text') == 'test'


@pytest.mark.django_db
def test_goal_update(auth_client, board_factory, goal_category_factory, goal_factory):
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
    goal = goal_factory(
        title='test',
        category=category,
        user_id=auth_client.session['_auth_user_id'],
    )
    response = auth_client.post(
        '/goals/goal_comment/create',
        data={
            'text': 'test',
            'goal': goal.id,
        }
    )
    pk = response.data.get('id')
    response = auth_client.patch(
        f'/goals/goal_comment/{pk}',
        data={
            'text': 'test2',
        },
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.data.get('text') == 'test2'


@pytest.mark.django_db
def test_goal_comment_delete(auth_client, board_factory, goal_category_factory, goal_factory):
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
    goal = goal_factory(
        title='test',
        category=category,
        user_id=auth_client.session['_auth_user_id'],
    )
    response = auth_client.post(
        '/goals/goal_comment/create',
        data={
            'text': 'test',
            'goal': goal.id,
        }
    )
    current_count = GoalComment.objects.all().count()
    pk = response.data.get('id')
    response = auth_client.delete(
        f'/goals/goal_comment/{pk}',
    )
    assert response.status_code == 204
    assert GoalComment.objects.all().count() == current_count - 1
