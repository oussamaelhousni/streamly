from kafka import KafkaProducer
import json

producer = KafkaProducer(
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    bootstrap_servers=["localhost:9092", "localhost:9093", "localhost:9094"],
)

future = producer.send("sysmtopms", [{"name": "oussama"}])
result = future.get(timeout=60)
