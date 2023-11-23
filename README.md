# mk-kafka-setup
This repository provides a Dockerized setup for Apache Kafka and Zookeeper. The setup includes a Docker Compose file for easy deployment, Python code files for interacting with Kafka, and a requirements.txt file for installing the required dependencies.


## Requirements
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python](https://www.python.org/downloads/) (for running Python code)

## Setup
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/mounikaran1/mk-kafka-docker.git
   ```

2. Navigate to the project directory:
    ```bash
    cd mk-kafka-setup
    ```
3. Build and start the Docker containers:
    ```bash
    docker compose up -d
    ```
4. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
