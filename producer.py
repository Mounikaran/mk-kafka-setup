from confluent_kafka import Producer
from json import dumps
from config import default_config

topic = "mk_topic"


def produce_messages():
    # Create Producer instance
    producer = Producer(default_config)

    # Produce messages to the topic
    for i in range(5):
        message = dumps(
            {
                "sourceId": "865",
                "campaignId": "-1",
                "sourceName": "MOBILE BANKING",
                "event": "sms_mt",
                "msisdn": "254727775779",
                "message": "Thank you for signing up for KCB Mobile Banking. You have successfully opened a Transactional account. Your Account name is KENNEDY WAFULA and Account number is 133****266. To start transacting, simply deposit money into your KCB account via Paybill 522522 or at a KCB Mtaani Agent today!\\n\\n#TESTSMS",
                "campaignName": None,
                "shortCode": "KCB",
                "referenceId": None,
                "timestamp": "2025-02-20T11:27:38.511826201",
            }
        )
        producer.produce(topic, key=str(i), value=message)
        producer.flush()

    print("Messages produced successfully.")


if __name__ == "__main__":
    # Produce messages
    produce_messages()
