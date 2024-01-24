from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError
import json
import os
import math
import logging
import constants
import yaml
import uuid


logger = logging.getLogger(__name__)
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)


def generate_unique_id():
    # unique ID for the receipt
    uuid_key =  str(uuid.uuid4())
    return uuid_key

def calculate_points(receipt_data):
    receipt_points = 0
    
    retailer_name = receipt_data["retailer"]
    purchase_date = receipt_data["purchaseDate"]
    purchase_time = receipt_data["purchaseTime"]
    total = receipt_data["total"]
    items = receipt_data["items"]

    receipt_points += retailer_points(retailer_name)
    receipt_points += date_and_time_points(purchase_date,purchase_time)
    receipt_points += amount_total_points(total_amount=float(total))
    receipt_points += items_points(items)

    logger.info(f"points accumulated -> {receipt_points}")
    return receipt_points


def retailer_points(retailer_name):
    points = 0
    for char in retailer_name:
        if char.isalnum():
            points += constants.SINGLE_POINT
    
    logger.info(f"retailer points {points}")
    return points

def date_and_time_points(purchase_date,purchase_time):
    points = 0
    date_tokens = purchase_date.split("-")
    day = int(date_tokens[2])
    if day%2 != 0:
        points += constants.ODD_DAY_POINTS
    time_tokens = purchase_time.split(":")
    hour = time_tokens[0]
    if hour>="14" and hour<"16":
        points += constants.TIME_2_TO_4_POINTS
    
    logger.info(f"date time points {points}")
    return points
    

def amount_total_points(total_amount):
    points = 0
    if total_amount == int(total_amount):
        points += constants.NO_CENT_POINTS
        
    if total_amount % 0.25 == 0:
        points += constants.QUARTER_DOLLAR_MULTIPLE_POINTS

    logger.info(f"amount total points {points}")
    return points

def items_points(items):
    points = 0
    items_count = len(items)
    points += (items_count//2) * 5
    for item in items:
        price = float(item["price"])
        desc = item["shortDescription"]
        desc = desc.strip()
        if len(desc) % 3 == 0:
            price = price * 0.2
            points += math.ceil(price)

    logger.info(f"items points {points}")
    return points

def load_schema_file(schema_file):
    if not schema_file:
        raise FileNotFoundError
    
    json_file_path = current_directory + os.sep + schema_file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    global schema
    schema = data

def validate_receipt(receipt_data):
    try:
        if not schema:
            raise Exception("validation schema not found")
        
        validate(instance=receipt_data, schema=schema)
        return True
    except ValidationError as e:
        logger.info(constants.INVALID_RECEIPT_SCHEMA)
        return False  # Validation failed
    

def setup_config():
    yaml_file_path = current_directory + os.sep + constants.CONFIG_FILE

    with open(yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)
        if "log_file" not in yaml_data:
            raise Exception("log file not found in config")
        setup_logging(request_logs_file=yaml_data["log_file"])

        if "schema_file" not in yaml_data:
            raise Exception("input schema file not found in config")
        load_schema_file(schema_file=yaml_data["schema_file"])


def setup_logging(request_logs_file):
    if not request_logs_file:
        raise FileNotFoundError
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    log_file = current_directory + os.sep + request_logs_file

    if os.path.exists(log_file):
        os.remove(log_file)

    file_handler = logging.FileHandler(log_file)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)