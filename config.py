bootstrap_servers = "localhost:9092"
group_id = "mk"
default_config = {
    "bootstrap.servers": bootstrap_servers,
}
consumer_config = {
    **default_config,
    "group.id": group_id,
    "auto.offset.reset": "earliest",  # Start reading from the beginning of the topic if no offset is stored
}
