"""
Tests for unregister endpoints.
Following the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


def test_unregister_success(client):
    """
    Test that a student can successfully unregister from an activity.
    
    AAA Pattern:
    - Arrange: Choose an activity with existing participants
    - Act: DELETE /activities/{activity_name}/unregister
    - Assert: Response status is 200 and success message is returned
    """
    # Arrange
    activity_name = "Programming Class"
    participant_email = "emma@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={participant_email}",
        params={"email": participant_email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert participant_email in data["message"]
    assert activity_name in data["message"]


def test_unregister_removes_participant(client):
    """
    Test that unregistering removes the student from the participants list.
    
    AAA Pattern:
    - Arrange: Get initial participant count
    - Act: DELETE to unregister, then GET /activities
    - Assert: Student email is no longer in the participants list
    """
    # Arrange
    activity_name = "Gym Class"
    participant_email = "john@mergington.edu"
    
    # Get initial state
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[activity_name]["participants"].copy()
    assert participant_email in initial_participants
    
    # Act
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={participant_email}",
        params={"email": participant_email}
    )
    
    # Get updated activities
    updated_response = client.get("/activities")
    updated_participants = updated_response.json()[activity_name]["participants"]
    
    # Assert
    assert unregister_response.status_code == 200
    assert participant_email not in updated_participants
    assert len(updated_participants) == len(initial_participants) - 1


def test_unregister_nonexistent_activity_returns_404(client):
    """
    Test that unregistering from a non-existent activity returns 404.
    
    AAA Pattern:
    - Arrange: Prepare an invalid activity name
    - Act: DELETE /activities/{invalid_name}/unregister
    - Assert: Response status is 404 and error detail is provided
    """
    # Arrange
    invalid_activity = "Nonexistent Activity"
    test_email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{invalid_activity}/unregister?email={test_email}",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_not_registered_returns_400(client):
    """
    Test that unregistering when not registered returns 400 error.
    
    AAA Pattern:
    - Arrange: Choose an activity and email that's not in its participants list
    - Act: DELETE /activities/{activity_name}/unregister with non-registered email
    - Assert: Response status is 400 and error detail is provided
    """
    # Arrange
    activity_name = "Art Club"
    non_registered_email = "notstudent@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={non_registered_email}",
        params={"email": non_registered_email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not registered" in data["detail"].lower()
