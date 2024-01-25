"""
This module contains a few pytests to unit test helper methods.
"""


import pytest
import json,os
from helper import (
    generate_unique_id,
    retailer_points,
    date_and_time_points,
    amount_total_points,
    items_points,
    load_schema_file,
)

receipt_data = {
    "retailer": "TestRetailer",
    "purchaseDate": "2024-01-24",
    "purchaseTime": "15:30",
    "total": "25.50",
    "items": [
        {"price": "10.00", "shortDescription": "Item1"},
        {"price": "15.50", "shortDescription": "Item2"},
    ],
}


def test_generate_unique_id():
    unique_id = generate_unique_id()
    assert isinstance(unique_id, str)

def test_retailer_points():
    points = retailer_points("TestRetailer")
    assert points > 0

def test_date_and_time_points():
    points = date_and_time_points("2024-01-24", "15:30")
    assert points > 0

def test_amount_total_points():
    points = amount_total_points(25.50)
    assert points > 0

def test_items_points():
    points = items_points(receipt_data["items"])
    assert points > 0

def test_load_schema_file():
    with pytest.raises(FileNotFoundError):
        load_schema_file("nonexistent_schema.json")



