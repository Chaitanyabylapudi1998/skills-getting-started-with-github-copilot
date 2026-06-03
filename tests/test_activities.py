"""Tests for the GET /activities endpoint."""

import pytest


class TestGetActivities:
    """Test suite for retrieving activities."""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activities.
        
        Arrange: Client is ready to make requests
        Act: Make GET request to /activities
        Assert: Response status is 200 and all 9 activities are returned
        """
        # Arrange: (implicit in fixture)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Basketball Team" in activities

    def test_get_activities_returns_correct_structure(self, client):
        """Test that activity objects have correct structure.
        
        Arrange: Client is ready to make requests
        Act: Make GET request to /activities
        Assert: Each activity has required fields
        """
        # Arrange: (implicit in fixture)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        activities = response.json()
        chess_club = activities["Chess Club"]
        
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)

    def test_get_activities_contains_initial_participants(self, client):
        """Test that activities contain their initial participants.
        
        Arrange: Client is ready to make requests
        Act: Make GET request to /activities
        Assert: Chess Club has initial participants
        """
        # Arrange: (implicit in fixture)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        activities = response.json()
        chess_club = activities["Chess Club"]
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]
