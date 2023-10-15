# Nginx Kafka Logging Pipeline

## Overview

This project sets up a logging pipeline that collects log data from Nginx, sends it to Kafka, and provides a way to query and analyze the metrics.

## Architecture

![Pipeline Architecture](https://github.com/afzouni/Nginx-Kafka-Loging-Pipeline/assets/7107254/837fb59d-e776-4c68-8829-7c0276622c60)

## Deployment

To deploy the pipeline, use the following command:

```bash
docker-compose up -d
```

## How to Use
### Get All Metrics
To retrieve all available metrics, make a GET request to the `/all` endpoint:
```bash
curl http://127.0.0.1:5001/all
```

### Get Metrics for a Specific Hour
To get metrics for a specific hour, use the `/metrics` endpoint with the datetime parameter. Replace `<datetime>` with the desired timestamp:

```bash
curl "http://127.0.0.1:5001/metrics?datetime=<datetime>"
```
Replace `<datetime>` with a timestamp in the format "YYYY-MM-DDTHH:MM:SS".

