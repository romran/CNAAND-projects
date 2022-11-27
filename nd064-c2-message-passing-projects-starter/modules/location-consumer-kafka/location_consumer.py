import os
import json

from kafka import KafkaConsumer
from sqlalchemy import create_engine

KAFKA_URL = os.environ["KAFKA_URL"]
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

location_consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=[KAFKA_URL])
db_engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)

def save_location(location, db_engine):
    connection = db_engine.connect()
    cursor = connection.cursor()
    id = int(location['id'])
    person_id = int(location["person_id"])
    coordinate = str(location["coordinate"])
    creation_time = str(location["creation_time"])

    location_insert = "INSERT INTO location (id, person_id, coordinate, creation_time) VALUES ({}, {}, {}, {})".format(
        id, person_id, coordinate, creation_time)
    cursor.execute(location_insert)


for location in location_consumer:
    location_message = json.loads(location.value.decode('utf-8'))
    print(location_message)
    save_location(location_message, db_engine)  