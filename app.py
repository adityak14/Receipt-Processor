from flask import Flask, request, jsonify, abort
from uuid import uuid4
import math
import re
import datetime

app = Flask(__name__)

RECEIPT_DATA = {}  # key: receipt_id (string), Value: points (int)


@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    """
    Path: /receipts/process
    Method: POST
    Payload: Receipt JSON
    Response: JSON containing an id for the receipt.
    """

    if not request.is_json:
        return abort(400, description="The receipt is invalid. Please verify input.")

    data = request.get_json()

    required_fields = ["retailer", "purchaseDate", "purchaseTime", "items", "total"]
    for field in required_fields:
        if field not in data:
            return abort(400, description="The receipt is invalid. Please verify input.")

    retailer = data["retailer"]
    purchase_date = data["purchaseDate"]
    purchase_time = data["purchaseTime"]
    items = data["items"]
    total_str = data["total"]

    # Validating the input fields.
    if not isinstance(items, list) or len(items) == 0:
        return abort(400, description="The receipt is invalid. Please verify input.")

    for item in items:
        if "shortDescription" not in item or "price" not in item:
            return abort(400, description="The receipt is invalid. Please verify input.")

    try:
        total = float(total_str)
    except ValueError:
        return abort(400, description="The receipt is invalid. Please verify input.")

    try:
        date_parts = purchase_date.split("-")
        if len(date_parts) != 3:
            return abort(400, description="The receipt is invalid. Please verify input.")
        year, month, day = map(int, date_parts)

        time_parts = purchase_time.split(":")
        if len(time_parts) != 2:
            return abort(400, description="The receipt is invalid. Please verify input.")
        hour, minute = map(int, time_parts)

        _ = datetime.datetime(year, month, day, hour, minute)
    except ValueError:
        return abort(400, description="The receipt is invalid. Please verify input.")

    # Computing points from the input data.
    points = compute_points(
        retailer=retailer,
        total=total,
        purchase_day=day,
        purchase_hour=hour,
        purchase_minute=minute,
        items=items
    )

    receipt_id = str(uuid4())
    RECEIPT_DATA[receipt_id] = {"points": points}

    return jsonify({"id": receipt_id}), 200


@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    """
    Path: /receipts/{id}/points
    Method: GET
    Response: A JSON object containing the number of points awarded.
    """
    if receipt_id not in RECEIPT_DATA:
        return abort(404, description="No receipt found for that ID.")
    
    return jsonify({"points": RECEIPT_DATA[receipt_id]["points"]}), 200


def compute_points(retailer, total, purchase_day, purchase_hour, purchase_minute, items):
    """
    Function for calculating the points based on the rules.
    """

    points = 0

    # 1 point per alphanumeric char in retailer name.
    for ch in retailer:
        if ch.isalnum():
            points += 1

    # 50 points if total is a round dollar amount with no cents.
    if total.is_integer():
        points += 50

    # 25 points if total is multiple of 0.25.
    if round(total * 100) % 25 == 0:
        points += 25

    # 5 points for every two items on the receipt.
    points += (len(items) // 2) * 5

    # 6 points if the day in the purchase date is odd.
    if purchase_day % 2 == 1:
        points += 6

    # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    if purchase_hour >= 14 and purchase_hour < 16:
        points += 10

    # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. 
    for item in items:
        desc = item["shortDescription"].strip()
        price = float(item["price"])
        if len(desc) % 3 == 0:
            points += math.ceil(price * 0.2)

    return points


# Error Handling.
@app.errorhandler(400)
def bad_request(e):
    return jsonify(error="The receipt is invalid. Please verify input."), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify(error="No receipt found for that ID."), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
