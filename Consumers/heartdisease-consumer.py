from kafka import KafkaConsumer
import json
from cursor import cursor, connection

# Kafka configuration
topic = "heartdisease"
heartdisease = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
    "target",
]

add_heartdisease = (
    f"INSERT INTO {topic} "
    f"({', '.join(heartdisease)}) "
    f"VALUES ({', '.join(['%s' for item in heartdisease])})"
)

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
        print("received")
        try:
            print("hi a sat")
            data_length = len(data_dict[list(data_dict.keys())[0]])
            print("hi 2 asat", data_length)
            for i in range(data_length):
                streamed_dict = {}
                for key, value in data_dict.items():
                    streamed_dict[key] = value[i]
                cursor.execute(add_heartdisease, tuple(streamed_dict.values()))
            print("la asat")
        except:
            for key in data_dict.keys():
                try:
                    data_dict[key] = float(data_dict[key])
                except:
                    pass
            # print(f"Received message: {data_dict}")
            # print(f"data type: {type(data_dict)}")
            cursor.execute(add_heartdisease, tuple(data_dict.values()))
        connection.commit()

        print(f"Received message")
        print(f"data type: {type(data_dict)}")
except KeyboardInterrupt:
    # This allows you to stop the script using Ctrl+C while it's running
    print("Script interrupted by user.")
finally:
    # Close the consumer when done
    consumer.close()
