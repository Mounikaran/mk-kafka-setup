from confluent_kafka import Consumer
from json import loads

from config import consumer_config

# Create Consumer instance
consumer = Consumer(consumer_config)

topics = ["kcb-invite-messages", "mk_topic"]

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
                    print("\n\nMessage received", message.topic())
                    print("Message: ", message.value())
                    # Decode bytes to string and parse JSON to dict
                    # raw_message = message.value().decode('utf-8')
                    # dict_message = loads(message.value())
                    # print("Message as dictionary: ", dict_message)
                    # print("Message key: ", dict_message['key'])
                    # print("Message key: ", dict_message['key'])
                    # print("Message value: ", dict_message['value'])

    except KeyboardInterrupt:
        pass
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


if __name__ == "__main__":
    print("Press Control + C to exit")
    consume_messages()
