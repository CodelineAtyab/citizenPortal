import utils.transform


def test_execute_returns_required_keys():
    """Test that execute function returns data with all required schema keys."""
    # Arrange: Create mock base_result data
    base_result = [
        {
            "name": "Luke Skywalker",
            "height": "172",
            "mass": "77",
            "hair_color": "blond",
            "skin_color": "fair",
            "eye_color": "blue",
        },
        {
            "name": "Darth Vader",
            "height": "202",
            "mass": "136",
            "hair_color": "none",
            "skin_color": "white",
            "eye_color": "yellow",
        }
    ]
    
    # Arrange: Create mock latest_result data with additional fields
    latest_result = [
        {
            "birth_year": "19BBY",
            "gender": "male",
            "homeworld": "https://swapi.dev/api/planets/1/",
            "created": "2014-12-09T13:50:51.644000Z",
            "edited": "2014-12-20T21:17:56.891000Z",
            "url": "https://swapi.dev/api/people/1/"
        },
        {
            "birth_year": "41.9BBY",
            "gender": "male",
            "homeworld": "https://swapi.dev/api/planets/1/",
            "created": "2014-12-10T15:18:20.704000Z",
            "edited": "2014-12-20T21:17:50.313000Z",
            "url": "https://swapi.dev/api/people/4/"
        }
    ]
    
    # Define required keys from the schema
    required_keys = [
        "name",
        "height",
        "mass",
        "hair_color",
        "skin_color",
        "eye_color",
        "birth_year",
        "gender",
        "homeworld",
        "created",
        "edited",
        "url"
    ]
    
    # Act: Execute the transformation
    result = utils.transform.execute(base_result, latest_result)
    
    # Assert: Verify result is a list
    assert isinstance(result, list), "Result should be a list"
    
    # Assert: Verify each item has all required keys
    for person in result:
        assert isinstance(person, dict), "Each item in result should be a dictionary"
        for key in required_keys:
            assert key in person, f"Missing required key: {key}"
    
    # Assert: Verify the correct number of items
    assert len(result) == 2, "Result should contain 2 characters"


def test_execute_merges_data_correctly():
    """Test that execute function correctly merges base and latest results."""
    # Arrange
    base_result = [
        {
            "name": "Luke Skywalker",
            "height": "172",
            "mass": "77",
        }
    ]
    
    latest_result = [
        {
            "gender": "male",
            "homeworld": "https://swapi.dev/api/planets/1/",
        }
    ]
    
    # Act
    result = utils.transform.execute(base_result, latest_result)
    
    # Assert: Verify data was merged correctly
    assert result[0]["name"] == "Luke Skywalker"
    assert result[0]["height"] == "172"
    assert result[0]["mass"] == "77"
    assert result[0]["gender"] == "male"
    assert result[0]["homeworld"] == "https://swapi.dev/api/planets/1/"


def test_execute_with_empty_lists():
    """Test that execute function handles empty lists correctly."""
    # Arrange
    base_result = []
    latest_result = []
    
    # Act
    result = utils.transform.execute(base_result, latest_result)
    
    # Assert
    assert isinstance(result, list), "Result should be a list"
    assert len(result) == 0, "Result should be empty"
