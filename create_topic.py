import sys
import time

from confluent_kafka.admin import AdminClient, NewTopic

from config import default_config


# Function to create a topic and check its status
def create_and_check_topics(topics):
    # Create AdminClient instance
    admin_client = AdminClient(default_config)

    for topic in topics:
        # Define the topic configuration (customize based on your requirements)
        topic_config = {
            'cleanup.policy': 'delete',
            'compression.type': 'lz4',
            'retention.ms': '3600000'
        }

        # Create NewTopic instance
        new_topic = NewTopic(topic, num_partitions=3, replication_factor=1, config=topic_config)

        # Create topics
        admin_client.create_topics([new_topic])

        print(f"Topic '{topic}' creation initiated.")

    # Check topic creation status
    for topic in topics:
        while True:
            topics_metadata = admin_client.list_topics(timeout=10).topics
            if topic in topics_metadata:
                print(f"Topic '{topic}' created successfully.")
                break
            else:
                print(f"Waiting for topic '{topic}' to be created...")
                time.sleep(5)

if __name__ == "__main__":
    # Get topics from command line arguments
    topics_from_args = sys.argv[1:]

    if not topics_from_args:
        print("Usage: python script.py topic1 topic2 ...")
        sys.exit(1)

    # Create and check the specified topics
    create_and_check_topics(topics_from_args)