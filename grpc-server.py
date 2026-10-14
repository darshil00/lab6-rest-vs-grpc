#!/usr/bin/env python3

import argparse
import base64
import io
from concurrent import futures

import grpc
from PIL import Image

import lab6_pb2
import lab6_pb2_grpc


class Lab6Service(lab6_pb2_grpc.Lab6ServiceServicer):

    def Add(self, request, context):
        result = request.a + request.b

        return lab6_pb2.addReply(
            sum=result
        )

    def RawImage(self, request, context):
        try:
            img = Image.open(io.BytesIO(request.img))

            return lab6_pb2.imageReply(
                width=img.width,
                height=img.height
            )

        except Exception:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Invalid image data"
            )

    def DotProduct(self, request, context):
        a = request.a
        b = request.b

        if len(a) != len(b):
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Vectors must have equal length"
            )

        result = sum(
            x * y for x, y in zip(a, b)
        )

        return lab6_pb2.dotProductReply(
            dotproduct=result
        )

    def JsonImage(self, request, context):
        try:
            image_bytes = base64.b64decode(
                request.img,
                validate=True
            )

            img = Image.open(
                io.BytesIO(image_bytes)
            )

            return lab6_pb2.imageReply(
                width=img.width,
                height=img.height
            )

        except Exception:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Invalid Base64 image data"
            )


def serve(port):
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ("grpc.max_receive_message_length", 16 * 1024 * 1024),
            ("grpc.max_send_message_length", 16 * 1024 * 1024)
        ]
    )

    lab6_pb2_grpc.add_Lab6ServiceServicer_to_server(
        Lab6Service(),
        server
    )

    server.add_insecure_port(
        f"0.0.0.0:{port}"
    )

    server.start()

    print(f"gRPC server running on port {port}", flush=True)

    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Lab 6 gRPC server"
    )

    parser.add_argument(
        "-p", "--port",
        type=int,
        default=50051
    )

    args = parser.parse_args()

    serve(args.port)
