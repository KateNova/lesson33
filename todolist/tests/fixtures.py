from datetime import date

import pytest


@pytest.fixture()
@pytest.mark.django_db
def auth_client(client, django_user_model):
    username = 'kate'
    password = '123qwe'
    django_user_model.objects.create_user(
        username=username,
        password=password,
    )
    client.login(username=username, password=password)
    return client
