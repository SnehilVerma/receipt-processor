from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError
import json
import os
import uuid
import math

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
app = Flask(__name__)


points_storage = {}

@app.route('/receipts/process', methods=['POST'])
def process_receipts():
    receipt_data = request.json
    
    receipt_valid = validate_receipt(receipt_data)
    if not receipt_valid:
        return jsonify({'description': "The receipt is invalid"}), 400

    points = calculate_points(receipt_data=receipt_data)
    
    receipt_id = str(uuid.uuid4()) # unique ID for the receipt

    points_storage[receipt_id] = points

    return jsonify({'id': receipt_id})


@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points_for_receipt(receipt_id):

    if receipt_id not in points_storage:
        return jsonify({'description': 'No receipt found for that id'}), 404

    points = points_storage[receipt_id]

    return jsonify({'points': points})

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

    print(f"points accumulated -> {receipt_points}")
    return receipt_points
    


def retailer_points(retailer_name):
    points = 0
    for char in retailer_name:
        if char.isalnum():
            points += 1
    
    # print(f"retailer points {points}")
    return points

def date_and_time_points(purchase_date,purchase_time):
    points = 0
    date_tokens = purchase_date.split("-")
    day = int(date_tokens[2])
    if day%2 != 0:
        points += 6
    time_tokens = purchase_time.split(":")
    hour = time_tokens[0]
    if hour>="14" and hour<"16":
        points += 10
    
    # print(f"date time {points}")
    return points
    

def amount_total_points(total_amount):
    points = 0
    if total_amount == int(total_amount):
        points += 50
        points += 25 #round dollar amount will always be a multiple of 0.25
        # print(f"total points {points}")
        return points
    if total_amount % 0.25 == 0:
        points = 25
        # print(f"total points {points}")
        return points

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

    # print(f"items points {points}")
    return points

def load_schema_file():
    json_file_path = current_directory + os.sep + "receipt_schema_2.json"
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    return data

def validate_receipt(receipt_data):
    schema = load_schema_file()
    try:
        validate(instance=receipt_data, schema=schema)
        return True  # Validation successful
    except ValidationError as e:
        # print(f"Validation error: {e}")
        return False  # Validation failed


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000,debug=True)
