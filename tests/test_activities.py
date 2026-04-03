"""
Tests for activity listing endpoints.
Following the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """
    Test that GET /activities returns all available activities.
    
    AAA Pattern:
    - Arrange: TestClient is provided by conftest fixture
    - Act: Make GET request to /activities
    - Assert: Response status is 200 and contains all activities
    """
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Soccer Club",
        "Art Club",
        "Drama Club",
        "Debate Club",
        "Science Club"
    ]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities_data = response.json()
    assert isinstance(activities_data, dict)
    for activity_name in expected_activities:
        assert activity_name in activities_data


def test_get_activities_returns_participants(client):
    """
    Test that each activity in the response includes a participants list.
    
    AAA Pattern:
    - Arrange: TestClient is provided by conftest fixture
    - Act: Make GET request to /activities
    - Assert: Each activity has a participants list
    """
    # Arrange (implicit from conftest)
    
    # Act
    response = client.get("/activities")
    activities_data = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_info in activities_data.items():
        assert "participants" in activity_info
        assert isinstance(activity_info["participants"], list)
        assert "description" in activity_info
        assert "schedule" in activity_info
        assert "max_participants" in activity_info


def test_root_redirects_to_static(client):
    """
    Test that GET / redirects to /static/index.html.
    
    AAA Pattern:
    - Arrange: TestClient is provided by conftest fixture
    - Act: Make GET request to /
    - Assert: Response is a redirect to /static/index.html
    """
    # Arrange (implicit from conftest)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
