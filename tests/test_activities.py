def test_get_activities_returns_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "description" in payload["Chess Club"]
    assert "schedule" in payload["Chess Club"]
    assert "max_participants" in payload["Chess Club"]
    assert "participants" in payload["Chess Club"]


def test_signup_for_activity_success(client):
    email = "new.student@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}

    verify = client.get("/activities")
    assert email in verify.json()["Chess Club"]["participants"]


def test_signup_for_activity_already_signed_up(client):
    email = "michael@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_not_found(client):
    response = client.post(
        "/activities/Nonexistent Club/signup",
        params={"email": "test@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_success(client):
    email = "michael@mergington.edu"

    response = client.delete("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}

    verify = client.get("/activities")
    assert email not in verify.json()["Chess Club"]["participants"]


def test_unregister_from_activity_not_signed_up(client):
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "not-registered@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_from_activity_not_found(client):
    response = client.delete(
        "/activities/Nonexistent Club/signup",
        params={"email": "test@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
