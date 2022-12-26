import pytest

from goals.models import (
    BoardParticipant,
    Board
)


@pytest.mark.django_db
def test_board_create(auth_client):
    data = {
        'title': 'test'
    }
    response_create = auth_client.post(
        '/goals/board/create',
        data=data,
        format='json',
    )
    pk = response_create.data.get('id')
    response_check = auth_client.get(f'/goals/board/{pk}')

    assert response_create.status_code == 201
    assert response_create.data.get('title') == data['title']
    assert response_check.status_code == 200
    assert response_check.data.get('title') == data['title']


@pytest.mark.django_db
def test_board_list(auth_client, board_factory):
    boards_count = 10
    boards = board_factory.create_batch(
        size=boards_count,
        title='test'
    )
    for board in boards:
        BoardParticipant.objects.create(
            user_id=auth_client.session['_auth_user_id'],
            board=board
        )
    response = auth_client.get(
        '/goals/board/list',
        format='json'
    )

    assert response.status_code == 200
    assert len(response.data) == boards_count
    for item in response.data:
        assert item.get('title') == 'test'


@pytest.mark.django_db
def test_board_update(auth_client):
    data = {
        'title': 'test'
    }
    response = auth_client.post(
        '/goals/board/create',
        data=data,
        format='json',
    )
    pk = response.data.get('id')
    response = auth_client.put(
        f'/goals/board/{pk}',
        data={
            'title': 'test2',
            'participants': []
        },
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.data.get('title') == 'test2'


@pytest.mark.django_db
def test_board_delete(auth_client):
    data = {
        'title': 'test'
    }
    response = auth_client.post(
        '/goals/board/create',
        data=data,
        format='json',
    )
    current_count = Board.objects.filter(is_deleted=False).count()
    pk = response.data.get('id')
    response = auth_client.delete(
        f'/goals/board/{pk}',
    )
    assert response.status_code == 204
    assert Board.objects.filter(is_deleted=False).count() == current_count - 1
