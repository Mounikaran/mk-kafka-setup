from confluent_kafka.admin import AdminClient

from config import default_config


def list_topics():
    # Create AdminClient instance
    admin_client = AdminClient(default_config)

    # List topics
    topics = admin_client.list_topics().topics
    print(f"Topics: {topics}")

if __name__ == "__main__":
    list_topics()