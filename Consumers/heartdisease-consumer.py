from kafka import KafkaConsumer
import json

# Kafka configuration
topic = "symptoms"

# Create a Kafka consumer
consumer = KafkaConsumer(
    topic, bootstrap_servers=["localhost:9092", "localhost:9093", "localhost:9094"]
)

# Continuously consume messages
try:
    for message in consumer:
        # Process the Kafka message here
        # Convert the byte data to a string and then parse it into a dictionary
        data_str = message.value.decode(
            "utf-8"
        )  # Decode the bytes to a string (assuming UTF-8 encoding)
        data_dict = json.loads(data_str)
        print(f"Received message: {data_dict['Name']}")
        print(f"data type: {type(data_dict)}")
except KeyboardInterrupt:
    # This allows you to stop the script using Ctrl+C while it's running
    print("Script interrupted by user.")
finally:
    # Close the consumer when done
    consumer.close()
