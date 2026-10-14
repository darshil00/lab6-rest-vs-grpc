#!/usr/bin/env python3

from flask import Flask, request, Response
import jsonpickle
from PIL import Image
import io
import argparse
import base64

# Initialize the Flask application
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)


@app.route('/api/add/<int:a>/<int:b>', methods=['GET', 'POST'])
def add(a, b):
    response = {'sum': str(a + b)}
    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )


@app.route('/api/rawimage', methods=['POST'])
def rawimage():
    r = request

    # Convert the data to a PIL image type so we can extract dimensions
    try:
        ioBuffer = io.BytesIO(r.data)
        img = Image.open(ioBuffer)

        response = {
            'width': img.size[0],
            'height': img.size[1]
        }
    except:
        response = {'width': 0, 'height': 0}

    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )


@app.route('/api/dotproduct', methods=['POST'])
def dotproduct():
    data = request.get_json()

    if not isinstance(data, dict):
        return {"error": "Invalid JSON payload"}, 400

    a = data.get("a")
    b = data.get("b")

    if not isinstance(a, list) or not isinstance(b, list):
        return {"error": "Both a and b must be lists"}, 400

    if len(a) != len(b):
        return {"error": "Vectors must have equal length"}, 400

    try:
        result = sum(float(x) * float(y) for x, y in zip(a, b))
    except (ValueError, TypeError):
        return {"error": "Vectors must contain numbers"}, 400

    return {"dotproduct": result}, 200

@app.route('/api/jsonimage', methods=['POST'])
def jsonimage():
    data = request.get_json()

    if not isinstance(data, dict) or not isinstance(data.get("image"), str):
        return {"error": "Missing Base64 image string"}, 400

    try:
        image_bytes = base64.b64decode(data["image"], validate=True)
        img = Image.open(io.BytesIO(image_bytes))

        response = {
            "width": img.size[0],
            "height": img.size[1]
        }

    except Exception:
        return {"error": "Invalid image data"}, 400

    return response, 200

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Flask REST server'
    )

    parser.add_argument(
        '-p', '--port',
        type=int,
        default=5000,
        help='Port on which to run the server (default: 5000)'
    )

    args = parser.parse_args()

    # Start Flask app
    app.run(host='0.0.0.0', port=args.port)
