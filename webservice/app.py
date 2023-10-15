import os
from flask import Flask, request, jsonify
import threading
from logging_config import logger
from kafka_consumer import *
from metrics import *

kafka_topic = os.getenv("KAFKA_TOPIC", "nginx")
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

app = Flask(__name__)

metrics_manager = MetricsManager()
kafka_service = KafkaConsumerService(kafka_topic, bootstrap_servers, metrics_manager)

@app.route('/all', methods=['GET'])
def get_all_metrics_data():
    all_metrics = metrics_manager.hourly_metrics

    all_metrics_json = {
        date: {
            hour: metrics.get_metrics()
            for hour, metrics in metrics_by_hour.items()
        }
        for date, metrics_by_hour in all_metrics.items()
    }

    return jsonify(all_metrics_json), 200

@app.route('/metrics', methods=['GET'])
def get_metrics():
    datetime_str = request.args.get('datetime')

    if not datetime_str:
        return jsonify({'error': 'Datetime parameter is required'}), 400

    try:
        metrics_data = metrics_manager.metrics(datetime_str)
        return jsonify(metrics_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

kafka_consumer_thread = threading.Thread(target=kafka_service.consume_kafka_topic)
kafka_consumer_thread.start()

if __name__ == '__main__':
    app.run(debug=True)
