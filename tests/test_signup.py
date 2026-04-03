"""
Tests for signup endpoints.
Following the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


def test_signup_success(client):
    """
    Test that a student can successfully sign up for an activity.
    
    AAA Pattern:
    - Arrange: Prepare a new email and activity name
    - Act: POST to /activities/{activity_name}/signup
    - Assert: Response status is 200 and success message is returned
    """
    # Arrange
    test_email = "newstudent@mergington.edu"
    activity_name = "Basketball Team"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={test_email}",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert test_email in data["message"]
    assert activity_name in data["message"]


def test_signup_adds_participant_to_list(client):
    """
    Test that signing up for an activity adds the student to its participants list.
    
    AAA Pattern:
    - Arrange: Get initial participant count and prepare test data
    - Act: POST to signup, then GET /activities
    - Assert: Student email is in the activity's participants list
    """
    # Arrange
    test_email = "anothernewemail@mergington.edu"
    activity_name = "Soccer Club"
    
    # Get initial state
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[activity_name]["participants"].copy()
    
    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={test_email}",
        params={"email": test_email}
    )
    
    # Get updated activities
    updated_response = client.get("/activities")
    updated_participants = updated_response.json()[activity_name]["participants"]
    
    # Assert
    assert signup_response.status_code == 200
    assert test_email in updated_participants
    assert len(updated_participants) == len(initial_participants) + 1


def test_signup_nonexistent_activity_returns_404(client):
    """
    Test that signing up for a non-existent activity returns 404.
    
    AAA Pattern:
    - Arrange: Prepare an invalid activity name
    - Act: POST to /activities/{invalid_name}/signup
    - Assert: Response status is 404 and error detail is provided
    """
    # Arrange
    test_email = "student@mergington.edu"
    invalid_activity = "Nonexistent Activity"
    
    # Act
    response = client.post(
        f"/activities/{invalid_activity}/signup?email={test_email}",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_duplicate_registration_returns_400(client):
    """
    Test that signing up twice with the same email returns 400 error.
    
    AAA Pattern:
    - Arrange: Choose an activity that already has participants
    - Act: Attempt to sign up with an email already in the participants list
    - Assert: Response status is 400 and error detail is provided
    """
    # Arrange
    activity_name = "Chess Club"
    existing_participant = "michael@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={existing_participant}",
        params={"email": existing_participant}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()
