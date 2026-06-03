"""Tests for the POST /activities/{activity_name}/signup endpoint."""

import pytest


class TestSignup:
    """Test suite for signing up participants for activities."""

    def test_successful_signup(self, client):
        """Test successful signup to an activity.
        
        Arrange: Client ready, Tennis Club has 2 participants initially
        Act: Sign up new participant to Tennis Club
        Assert: Response is 200 and participant is added
        """
        # Arrange
        activity_name = "Tennis Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == 3

    def test_signup_duplicate_student(self, client):
        """Test that duplicate signup returns error.
        
        Arrange: Michael is already signed up for Chess Club
        Act: Try to sign up Michael again for Chess Club
        Assert: Response is 400 with "already signed up" message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_activity_not_found(self, client):
        """Test signup to non-existent activity returns 404.
        
        Arrange: Client ready
        Act: Try to sign up to non-existent activity
        Assert: Response is 404 with "Activity not found" message
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_activity_full(self, client):
        """Test signup to full activity returns error.
        
        Arrange: Create activity with max_participants=1 and 1 participant
        Act: Try to sign up another participant
        Assert: Response is 400 with "Activity is full" message
        """
        # Arrange
        # We need to manipulate an activity to be full
        # Let's use Programming Class and temporarily reduce its capacity
        from src.app import activities
        
        activity_name = "Programming Class"
        # Reduce to 2 max participants (currently has 2), making it full
        activities[activity_name]["max_participants"] = 2
        email = "fulltest@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "Activity is full" in response.json()["detail"]

    def test_signup_multiple_participants_increases_count(self, client):
        """Test that multiple signups correctly increase participant count.
        
        Arrange: Basketball Team initially has 1 participant
        Act: Sign up two new participants
        Assert: Participant count increases to 3
        """
        # Arrange
        activity_name = "Basketball Team"
        emails = ["student1@mergington.edu", "student2@mergington.edu"]
        
        # Act
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Assert
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert len(activities[activity_name]["participants"]) == 3
        for email in emails:
            assert email in activities[activity_name]["participants"]
