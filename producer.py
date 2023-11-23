from confluent_kafka import Producer

from config import default_config

topic = "mk_topic"


def produce_messages():
    # Create Producer instance
    producer = Producer(default_config)

    # Produce messages to the topic
    for i in range(5):
        message = f"Message {i}"
        producer.produce(topic, key=str(i), value=message)
        producer.flush()

    print("Messages produced successfully.")


if __name__ == "__main__":
    # Produce messages
    produce_messages()
