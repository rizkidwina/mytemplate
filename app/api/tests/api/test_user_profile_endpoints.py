def test_create_my_profile(client) -> None:
    response = client.post(
        "/api/v1/users/me/profile",
        json={
            "display_name": "API Test User",
            "phone_number": "081234567890",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["display_name"] == "API Test User"
    assert data["phone_number"] == "081234567890"
    assert data["auth_user_id"] == "test-auth-user-001"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_my_profile(client) -> None:
    client.post(
        "/api/v1/users/me/profile",
        json={
            "display_name": "Get API Test",
        },
    )

    response = client.get(
        "/api/v1/users/me/profile",
    )

    assert response.status_code == 200
    assert response.json()["display_name"] == "Get API Test"


def test_get_nonexistent_profile(client) -> None:
    response = client.get(
        "/api/v1/users/me/profile",
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "USER_PROFILE_NOT_FOUND"


def test_create_duplicate_profile(client) -> None:
    payload = {
        "display_name": "Duplicate Test",
    }

    first_response = client.post(
        "/api/v1/users/me/profile",
        json=payload,
    )

    second_response = client.post(
        "/api/v1/users/me/profile",
        json=payload,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_update_my_profile(client) -> None:
    client.post(
        "/api/v1/users/me/profile",
        json={
            "display_name": "Before Update",
        },
    )

    response = client.patch(
        "/api/v1/users/me/profile",
        json={
            "display_name": "After Update",
        },
    )

    assert response.status_code == 200
    assert response.json()["display_name"] == "After Update"


def test_update_my_profile_phone_number(client) -> None:
    client.post(
        "/api/v1/users/me/profile",
        json={
            "display_name": "Phone Test",
            "phone_number": "081111111111",
        },
    )

    response = client.patch(
        "/api/v1/users/me/profile",
        json={
            "phone_number": None,
        },
    )

    assert response.status_code == 200
    assert response.json()["phone_number"] is None


def test_update_my_profile_empty_payload(client) -> None:
    client.post(
        "/api/v1/users/me/profile",
        json={
            "display_name": "Empty Payload Test",
        },
    )

    response = client.patch(
        "/api/v1/users/me/profile",
        json={},
    )

    assert response.status_code == 400


def test_delete_my_profile(client) -> None:
    client.post(
        "/api/v1/users/me/profile",
        json={
            "display_name": "Delete API Test",
        },
    )

    response = client.delete(
        "/api/v1/users/me/profile",
    )

    assert response.status_code == 204


def test_deleted_profile_cannot_be_retrieved(client) -> None:
    client.post(
        "/api/v1/users/me/profile",
        json={
            "display_name": "Delete Then Get",
        },
    )

    client.delete(
        "/api/v1/users/me/profile",
    )

    response = client.get(
        "/api/v1/users/me/profile",
    )

    assert response.status_code == 404


def test_create_profile_rejects_invalid_display_name(
    client,
) -> None:
    response = client.post(
        "/api/v1/users/me/profile",
        json={
            "display_name": "",
        },
    )

    assert response.status_code == 422
