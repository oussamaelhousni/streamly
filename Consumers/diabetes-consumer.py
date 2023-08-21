from cursor import cursor, connection
from kafka import KafkaConsumer
import json

# Kafka configuration
topic = "diabetes"
diabetes = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
    "Outcome",
]

# Create a Kafka consumer
consumer = KafkaConsumer(
    topic, bootstrap_servers=["localhost:9092", "localhost:9093", "localhost:9094"]
)

# query
add_diabetes = (
    f"INSERT INTO {topic} "
    f"({', '.join(diabetes)}) "
    f"VALUES ({', '.join(['%s' for item in diabetes])})"
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
        try:
            data_length = len(data_dict[list(data_dict.keys())[0]])
            for i in range(data_length):
                streamed_dict = {}
                for key, value in data_dict.items():
                    streamed_dict[key] = value[i]
                cursor.execute(add_diabetes, streamed_dict)
        except:
            for key in data_dict.keys():
                try:
                    data_dict[key] = float(data_dict[key])
                except:
                    pass
            print(f"Received message: {data_dict}")
            print(f"data type: {type(data_dict)}")
            cursor.execute(add_diabetes, tuple(data_dict.values()))
            connection.commit()
except KeyboardInterrupt:
    # This allows you to stop the script using Ctrl+C while it's running
    print("Script interrupted by user.")
finally:
    # Close the consumer when done
    consumer.close()
