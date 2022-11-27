import grpc
import location_pb2
import location_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:30010")
stub = location_pb2_grpc.LocationServiceStub(channel)

# Update this with desired payload
location = location_pb2.LocationMessage(
    id = 70,
    person_id = 8,
    coordinate = '010100000097FDBAD39D925EC0D00A0C59DDC64240',
    creation_time = '2020-07-07 10:47:06.000000',
)

response = stub.Create(location)