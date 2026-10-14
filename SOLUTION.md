# Lab 6 - REST vs gRPC Performance Comparison

All measurements are average milliseconds per operation.

## Performance Results

| Method | Local | Same-Zone | Different Region |
|---|---:|---:|---:|
| REST add | 2.707 | TBD | TBD |
| gRPC add | 0.944 | TBD | TBD |
| REST rawimg | 4.938 | TBD | TBD |
| gRPC rawimg | 6.738 | TBD | TBD |
| REST dotproduct | 3.231 | TBD | TBD |
| gRPC dotproduct | 1.406 | TBD | TBD |
| REST jsonimg | 26.497 | TBD | TBD |
| gRPC jsonimg | 19.512 | TBD | TBD |
| PING | 0.049 | TBD | TBD |

## Measurement Methodology

Localhost measurements were conducted using Google Cloud Shell.

Both REST and gRPC clients executed 1,000 requests per operation.
Average latency was calculated using Python's time.perf_counter().

The same image was used for both image operations.

The dot-product operation used two vectors of 100 random numbers.

Localhost network latency was measured using 10 ICMP ping requests.

## Localhost Observations

For lightweight operations such as addition and dot product, gRPC
showed lower average latency than REST.

For raw image processing, REST was faster in this experiment,
while gRPC was faster for the Base64 JSON image operation.

The measured latency includes RPC overhead, data serialization,
image processing, and Python client/server execution.

The effect of network distance will be evaluated using
same-zone and cross-region experiments.
