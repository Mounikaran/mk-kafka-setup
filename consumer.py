from confluent_kafka import Consumer

from config import consumer_config

# Create Consumer instance
consumer = Consumer(consumer_config)

topics = ["mk_topic"]

# Subscribe to topics
consumer.subscribe(topics)


def consume_messages():
    try:
        while True:
            # Poll for messages
            message = consumer.poll(1.0)
            if message:
                if message.error():
                    print(f"Consumer error : {message.error()}")
                else:
                    raw_message = message.value()
                    print("Message: ", raw_message)

    except KeyboardInterrupt:
        pass
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


if __name__ == "__main__":
    print("Press Control + C to exit")
    consume_messages()
