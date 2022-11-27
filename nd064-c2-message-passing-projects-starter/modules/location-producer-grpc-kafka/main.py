import time

from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc

from kafka import KafkaProducer
import os
import json

KAFKA_URL= os.environ["KAFKA_URL"]
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_URL)

class LocationServicer(location_pb2_grpc.LocationEventServiceServicer):

    def Create(self, request, context):
        request_value = {
            "id": request.id,
            "person_id": request.person_id,
            "coordinate": request.coordinate,
            "creation_time": request.creation_time,
        }
        print(request_value)

        encode_request_data = json.dumps(request_value, indent=2).encode('utf-8')
        kafka_producer.send(KAFKA_TOPIC, encode_request_data)

        return location_pb2.LocationMessage(**request_value)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationEventServiceServicer_to_server(LocationServicer(), server)

print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)