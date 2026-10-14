#!/usr/bin/env python3

import argparse
import base64
import random
import time
from pathlib import Path

import grpc
from PIL import Image
import io

import lab6_pb2
import lab6_pb2_grpc


IMAGE_FILE = Path(__file__).resolve().parent / "Flatirons_Winter_Sunrise_edit_2.jpg"


def doAdd(stub, debug=False):
    response = stub.Add(
        lab6_pb2.addMsg(a=5, b=10)
    )

    if response.sum != 15:
        raise ValueError("Incorrect addition result")

    if debug:
        print("Addition result:", response.sum)


def doRawImage(stub, image_bytes, expected_size, debug=False):
    response = stub.RawImage(
        lab6_pb2.rawImageMsg(img=image_bytes)
    )

    if (response.width, response.height) != expected_size:
        raise ValueError("Incorrect raw image dimensions")

    if debug:
        print("Raw image dimensions:", response.width, response.height)


def doDotProduct(stub, debug=False):
    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]

    response = stub.DotProduct(
        lab6_pb2.dotProductMsg(a=a, b=b)
    )

    expected = sum(
        float(lab6_pb2.dotProductMsg(a=[x]).a[0]) *
        float(lab6_pb2.dotProductMsg(b=[y]).b[0])
        for x, y in zip(a, b)
    )

    if abs(response.dotproduct - expected) > 1e-4:
        raise ValueError("Incorrect dot product result")

    if debug:
        print("Dot product:", response.dotproduct)


def doJsonImage(stub, encoded_image, expected_size, debug=False):
    response = stub.JsonImage(
        lab6_pb2.jsonImageMsg(img=encoded_image)
    )

    if (response.width, response.height) != expected_size:
        raise ValueError("Incorrect JSON image dimensions")

    if debug:
        print("JSON image dimensions:", response.width, response.height)


def main():
    parser = argparse.ArgumentParser(
        description="gRPC client for measuring server operations"
    )

    parser.add_argument(
        "host",
        help="IP address or hostname of the gRPC server"
    )

    parser.add_argument(
        "cmd",
        choices=["add", "rawImage", "dotProduct", "jsonImage"],
        help="Operation to perform"
    )

    parser.add_argument(
        "reps",
        type=int,
        help="Number of repetitions"
    )

    parser.add_argument(
        "-p", "--port",
        type=int,
        default=50051
    )

    parser.add_argument(
        "-d", "--debug",
        action="store_true"
    )

    args = parser.parse_args()

    if args.reps <= 0:
        parser.error("reps must be greater than zero")

    address = f"{args.host}:{args.port}"

    image_bytes = IMAGE_FILE.read_bytes()
    encoded_image = base64.b64encode(image_bytes).decode("ascii")

    with Image.open(io.BytesIO(image_bytes)) as img:
        expected_size = img.size

    print(f"Running {args.reps} reps against {address}")
    print(f"Operation: {args.cmd}")

    with grpc.insecure_channel(
        address,
        options=[
            ("grpc.max_send_message_length", 16 * 1024 * 1024),
            ("grpc.max_receive_message_length", 16 * 1024 * 1024)
        ]
    ) as channel:

        grpc.channel_ready_future(channel).result(timeout=30)

        stub = lab6_pb2_grpc.Lab6ServiceStub(channel)

        start = time.perf_counter()

        for _ in range(args.reps):

            if args.cmd == "add":
                doAdd(stub, args.debug)

            elif args.cmd == "rawImage":
                doRawImage(stub, image_bytes, expected_size, args.debug)

            elif args.cmd == "dotProduct":
                doDotProduct(stub, args.debug)

            elif args.cmd == "jsonImage":
                doJsonImage(stub, encoded_image, expected_size, args.debug)

        elapsed = time.perf_counter() - start

        average_ms = (elapsed / args.reps) * 1000

        print(f"Took {average_ms:.4f} ms per operation")


if __name__ == "__main__":
    main()
