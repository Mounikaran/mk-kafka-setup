import sys
import time
from confluent_kafka.admin import AdminClient, NewTopic, ConfigResource
from config import default_config


def clear_kafka_topics(topic_names):
    """
    Completely clears Kafka topics by deleting and recreating them.
    This is the most reliable way to ensure all messages are wiped and
    offsets are reset for all consumer groups.
    """
    admin_client = AdminClient(default_config)

    # 1. Fetch current metadata and configs
    print("Fetching topic metadata...")
    metadata = admin_client.list_topics(timeout=10)

    topics_to_process = []

    for topic_name in topic_names:
        if topic_name not in metadata.topics:
            print(f"Warning: Topic '{topic_name}' does not exist. Skipping.")
            continue

        topic_meta = metadata.topics[topic_name]
        num_partitions = len(topic_meta.partitions)
        # Take replication factor from the first partition
        replication_factor = (
            len(topic_meta.partitions[0].replicas) if num_partitions > 0 else 1
        )

        # Get topic configs
        resource = ConfigResource(ConfigResource.Type.TOPIC, topic_name)
        config_futures = admin_client.describe_configs([resource])

        # We'll try to preserve some important configs
        original_configs = {}
        try:
            configs = config_futures[resource].result()
            # Filter for non-default configs or common ones
            important_keys = [
                "cleanup.policy",
                "retention.ms",
                "retention.bytes",
                "compression.type",
                "max.message.bytes",
            ]
            for key in important_keys:
                if key in configs:
                    original_configs[key] = configs[key].value
        except Exception as e:
            print(f"Could not fetch configs for '{topic_name}': {e}")

        topics_to_process.append(
            {
                "name": topic_name,
                "num_partitions": num_partitions,
                "replication_factor": replication_factor,
                "configs": original_configs,
            }
        )

    if not topics_to_process:
        print("No existing topics found to clear.")
        return

    # 2. Delete the topics
    print(f"Deleting topics: {[t['name'] for t in topics_to_process]}...")
    delete_futures = admin_client.delete_topics(
        [t["name"] for t in topics_to_process], operation_timeout=30
    )

    for topic, future in delete_futures.items():
        try:
            future.result()
            print(f"Topic '{topic}' deletion initiated.")
        except Exception as e:
            print(f"Error deleting topic '{topic}': {e}")

    # 3. Wait for deletion to propagate
    print("Waiting for deletion to complete...")
    max_retries = 15
    for i in range(max_retries):
        current_metadata = admin_client.list_topics(timeout=10).topics
        still_exists = [
            t["name"] for t in topics_to_process if t["name"] in current_metadata
        ]
        if not still_exists:
            # Even if it's gone from metadata, sometimes the broker needs an extra second
            time.sleep(3)
            break
        print(f"Still waiting for: {still_exists} ({i+1}/{max_retries})")
        time.sleep(3)
    else:
        print("Error: Deletion took too long. Some topics might still exist.")

    # 4. Recreate the topics
    print("Recreating topics...")
    new_topics = [
        NewTopic(
            t["name"],
            num_partitions=t["num_partitions"],
            replication_factor=t["replication_factor"],
            config=t["configs"],
        )
        for t in topics_to_process
    ]

    create_futures = admin_client.create_topics(new_topics, operation_timeout=30)
    for topic, future in create_futures.items():
        try:
            future.result()
            print(
                f"Topic '{topic}' recreated successfully with {topics_to_process[0]['num_partitions']} partitions."
            )
        except Exception as e:
            print(f"Error recreating topic '{topic}': {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clear_topic_messages.py <topic1> <topic2> ...")
        sys.exit(1)

    clear_kafka_topics(sys.argv[1:])
