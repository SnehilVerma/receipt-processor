from flask import Flask, request, jsonify
from helper import calculate_points,validate_receipt, logger, setup_config, generate_unique_id
import constants

app = Flask(__name__)


points_storage = {}

@app.route('/receipts/process', methods=['POST'])
def process_receipts():
    receipt_data = request.json
    
    receipt_valid = validate_receipt(receipt_data)
    if not receipt_valid:
        return jsonify({'description': constants.INVALID_RECEIPT}), 400

    points = calculate_points(receipt_data=receipt_data)
    
    receipt_id = generate_unique_id() 

    points_storage[receipt_id] = points

    logger.info(f"{constants.VALID_RECEIPT} {points} , {receipt_id}")
    return jsonify({'id': receipt_id})


@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points_for_receipt(receipt_id):

    if receipt_id not in points_storage:
        return jsonify({'description': constants.INVALID_RECEIPT_ID}), 404

    points = points_storage[receipt_id]

    logger.info(f"{constants.VALID_RECEIPT_ID} {points}")
    return jsonify({'points': points})


if __name__ == '__main__':
    setup_config()
    app.run(host='0.0.0.0', port=6000,debug=True)
