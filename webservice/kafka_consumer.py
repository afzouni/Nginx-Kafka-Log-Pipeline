import json
from kafka import KafkaConsumer
from datetime import datetime
from metrics import MetricsManager
from typing import Any
from logging_config import logger
from kafka.errors import NoBrokersAvailable
import time

class KafkaConsumerService:
    def __init__(self, topic_name: str, bootstrap_servers: str, metrics_manager: MetricsManager):
        self.topic_name = topic_name
        self.bootstrap_servers = bootstrap_servers
        self.metrics_manager = metrics_manager

    def consume_kafka_topic(self) -> None:
        try:
            consumer = KafkaConsumer(self.topic_name, bootstrap_servers=self.bootstrap_servers)

            for message in consumer:
                try:
                    message_data = message.value.decode('utf-8')
                    logger.debug(message_data)
                    data = json.loads(message_data)

                    timestamp_str = data.get("timestamp")
                    upstream_response_time = data.get("upstream_response_time")

                    if timestamp_str and upstream_response_time:
                        timestamp = datetime.fromisoformat(timestamp_str)
                        upstream_response_time = float(upstream_response_time)
                        datetime_str = timestamp.strftime("%Y-%m-%dT%H:%M:%S")
                        
                        self.metrics_manager.record_response(datetime_str, upstream_response_time)

                        logger.info("Stored: %s - Upstream Response Time: %s", datetime_str, upstream_response_time)
                    else:
                        logger.warning("Invalid or missing data in the message")

                except Exception as e:
                    logger.error("Error processing message: %s", e)
        except NoBrokersAvailable as e:
            
            logger.error("Error connecting to Kafka: %s", str(e))
            time.sleep(10)  
