"""
Test suite for Haversine CLI Calculator

This test suite follows the Test-First Development principle from the 
Germaneering Lab constitution. Tests serve dual purpose:
1. Validating correctness of the haversine calculation implementation
2. Documenting expected behavior for educational reference

Test Organization:
- test_models.py: GeographicPoint validation and behavior
- test_calculator.py: Haversine formula accuracy and edge cases  
- test_validator.py: Input validation and error handling
- test_cli.py: Command-line interface integration tests

Run tests with:
    uv run -m unittest discover tests
    python -m unittest discover tests
"""