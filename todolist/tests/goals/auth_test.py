def test_no_auth_goal_list(client):
    response = client.get(
        '/goals/goal/list'
    )
    assert response.status_code == 403


def test_no_auth_board_list(client):
    response = client.get(
        '/goals/board/list'
    )
    assert response.status_code == 403


def test_no_auth_category_list(client):
    response = client.get(
        '/goals/goal_category/list'
    )
    assert response.status_code == 403


def test_auth_goal_list(auth_client):
    response = auth_client.get(
        '/goals/goal/list',
    )
    assert response.status_code == 200


def test_auth_board_list(auth_client):
    response = auth_client.get(
        '/goals/board/list',
    )
    assert response.status_code == 200


def test_auth_goal_category_list(auth_client):
    response = auth_client.get(
        '/goals/goal_category/list',
    )
    assert response.status_code == 200
