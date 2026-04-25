bootstrap_servers = "localhost:9092"
group_id = "mk"
default_config = {
    "bootstrap.servers": bootstrap_servers,
    # Message size configurations for large messages (2GB limit)
    # "message.max.bytes": 2147483647,
    # "receive.message.max.bytes": 2147483647,
    # "send.buffer.bytes": 104857600,
    # "receive.buffer.bytes": 104857600,
}
consumer_config = {
    **default_config,
    "group.id": group_id,
    "auto.offset.reset": "earliest",  # Start reading from the beginning of the topic if no offset is stored
    # Consumer-specific configurations for large messages
    "fetch.message.max.bytes": 2147483647,
    "max.partition.fetch.bytes": 2147483647,
}
