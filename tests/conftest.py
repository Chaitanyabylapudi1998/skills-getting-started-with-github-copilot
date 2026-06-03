"""Pytest configuration and shared fixtures for FastAPI tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for making requests to the FastAPI application."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to known state before each test.
    
    This fixture ensures test isolation by resetting the in-memory
    activities dictionary to a consistent state for each test.
    """
    # Store original activities
    test_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Join the competitive basketball team and develop athletic skills",
            "schedule": "Tuesdays and Thursdays, 4:30 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis techniques and compete in matches",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["james@mergington.edu", "lucas@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore various art mediums and develop creative skills",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["ava@mergington.edu"]
        },
        "Theater Club": {
            "description": "Perform in school plays and develop acting abilities",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["isabella@mergington.edu", "mia@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills through competitive debate",
            "schedule": "Mondays and Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 14,
            "participants": ["christopher@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["grace@mergington.edu", "hannah@mergington.edu"]
        }
    }
    
    # Clear and reset activities
    activities.clear()
    activities.update(test_activities)
    
    yield
    
    # Cleanup after test
    activities.clear()
    activities.update(test_activities)
