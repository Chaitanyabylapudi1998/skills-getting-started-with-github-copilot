"""Tests for the POST /activities/{activity_name}/remove endpoint."""

import pytest


class TestRemove:
    """Test suite for removing participants from activities."""

    def test_successful_removal(self, client):
        """Test successful removal of participant from activity.
        
        Arrange: Michael is in Chess Club (initial participant count: 2)
        Act: Remove Michael from Chess Club
        Assert: Response is 200 and participant is removed
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/remove",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == 1

    def test_remove_participant_not_enrolled(self, client):
        """Test removal of non-enrolled participant returns error.
        
        Arrange: Student not in any activity
        Act: Try to remove non-enrolled student
        Assert: Response is 400 with "not signed up" message
        """
        # Arrange
        activity_name = "Tennis Club"
        email = "notinclass@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/remove",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_remove_from_nonexistent_activity(self, client):
        """Test removal from non-existent activity returns 404.
        
        Arrange: Client ready
        Act: Try to remove from non-existent activity
        Assert: Response is 404 with "Activity not found" message
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/remove",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_remove_decreases_participant_count(self, client):
        """Test that removal decreases participant count.
        
        Arrange: Theater Club has 2 initial participants
        Act: Remove one participant
        Assert: Participant count decreases to 1
        """
        # Arrange
        activity_name = "Theater Club"
        email = "isabella@mergington.edu"
        
        activities_before = client.get("/activities").json()
        initial_count = len(activities_before[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/remove",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        
        activities_after = client.get("/activities").json()
        final_count = len(activities_after[activity_name]["participants"])
        assert final_count == initial_count - 1

    def test_remove_multiple_participants(self, client):
        """Test removing multiple participants from same activity.
        
        Arrange: Gym Class has 2 initial participants
        Act: Remove both participants
        Assert: Activity becomes empty
        """
        # Arrange
        activity_name = "Gym Class"
        emails = ["john@mergington.edu", "olivia@mergington.edu"]
        
        # Act
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/remove",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Assert
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert len(activities[activity_name]["participants"]) == 0

    def test_remove_then_signup_same_student(self, client):
        """Test that removed student can sign up again.
        
        Arrange: Daniel is in Chess Club
        Act: Remove Daniel, then sign him up again
        Assert: Signup succeeds and Daniel is back in activity
        """
        # Arrange
        activity_name = "Chess Club"
        email = "daniel@mergington.edu"
        
        # Act - Remove
        remove_response = client.post(
            f"/activities/{activity_name}/remove",
            params={"email": email}
        )
        assert remove_response.status_code == 200
        
        # Act - Sign up
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert signup_response.status_code == 200
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]
