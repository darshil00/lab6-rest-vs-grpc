
# Lab 6 - REST vs gRPC Performance Comparison

All measurements are average milliseconds per operation.

## Performance Results

| Method | Local | Same-Zone | Different Region |
|---|---:|---:|---:|
| REST add | 2.707 | 3.030 | 327.461 |
| gRPC add | 0.944 | 1.035 | 160.212 |
| REST rawimg | 4.938 | 7.057 | 1325.191 |
| gRPC rawimg | 6.738 | 8.766 | 198.604 |
| REST dotproduct | 3.231 | 3.611 | 352.218 |
| gRPC dotproduct | 1.406 | 1.600 | 161.417 |
| REST jsonimg | 26.497 | 29.856 | 1688.569 |
| gRPC jsonimg | 19.512 | 14.522 | 216.448 |
| PING | 0.049 | 0.420 | 140.981 |

## Measurement Methodology

The experiment compared four operations implemented using both REST and gRPC: addition, raw image processing, dot product, and Base64-encoded JSON image processing.

The localhost experiment was performed in Google Cloud Shell using 1,000 requests per operation.

The same-zone experiment used two Google Compute Engine `e2-standard-2` virtual machines in `us-west1-a`, with the client communicating with the server through its internal IP address. Each operation was repeated 1,000 times.

The cross-region experiment used the client VM in `us-west1-a` and a server VM in `europe-west3-a` (Frankfurt). Internal IP communication was used, and each operation was repeated 100 times.

All RPC timings were measured using Python's `time.perf_counter()` and reported as average milliseconds per operation.

The dot-product operation used vectors containing 100 randomly generated numbers between 0 and 1. Both image operations used the same Flatirons JPEG image, measuring 3004 x 1002 pixels.

Network latency was measured using 10 ICMP ping requests for each environment. The reported PING values represent average round-trip times.

## Observations

For lightweight operations such as addition and dot product, gRPC consistently achieved lower average latency than REST. On localhost, REST addition took 2.707 ms compared with 0.944 ms for gRPC.

In the same-zone experiment, network latency remained low, with an average ping of 0.420 ms. REST was faster for raw image processing, while gRPC was faster for addition, dot product, and JSON image processing.

The largest performance differences appeared in the cross-region experiment. Average network round-trip latency increased to 140.981 ms. REST addition required 327.461 ms per operation, while gRPC addition required 160.212 ms.

For raw image processing, REST required 1325.191 ms compared with 198.604 ms for gRPC. Similarly, JSON image processing required 1688.569 ms using REST compared with 216.448 ms using gRPC.

An important difference is connection management. The REST client used individual HTTP requests without an explicitly persistent session, whereas the gRPC client reused a single HTTP/2 connection for multiple requests. Reusing a connection can reduce connection-establishment overhead, particularly when communicating between geographically distant regions.

The results also reflect differences in serialization, payload transmission, image processing, and Python execution. Therefore, they should not be interpreted as measuring network protocol overhead alone.

Overall, the experiment demonstrated that network distance strongly affects RPC latency and that gRPC can provide substantial performance advantages, particularly for repeated requests across high-latency networks.
